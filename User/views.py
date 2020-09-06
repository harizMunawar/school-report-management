from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from User.forms import RegistrationForm, GuruForm, SiswaForm

from User.models import User, Siswa, Guru
from Kelas.models import Jurusan, Kelas
from Nilai.models import MataPelajaran, NilaiMataPelajaran

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from collections import Counter

@login_required
def dashboard(request):
    context = {}
    active_user = User.objects.get(nomor_induk = request.user.nomor_induk)
    if active_user.level == 'G':  
        try:      
            guru = Guru.objects.get(user=active_user)
            kelas = Kelas.objects.get(walikelas=guru.id)
            list_siswa = Siswa.objects.filter(kelas=kelas.id)            
        except ObjectDoesNotExist:
            kelas = None
            list_siswa = None

        context = {
            'siswa': list_siswa,
            'kelas': kelas,
        }

    if active_user.level == 'S':
        try:
            siswa = Siswa.objects.get(user=active_user)
            kelas = Kelas.objects.get(nama=siswa.kelas)
            walikelas = Guru.objects.get(nama=kelas.walikelas)
            matapelajaran = MataPelajaran.objects.values('id').filter(kelas=kelas)[::1]
            list_pelajaran = []
            pel_nilai = []

            for pelajaran in matapelajaran:
                list_pelajaran.append(pelajaran['id'])

            for pelajaran in list_pelajaran:
                pel = MataPelajaran.objects.values('nama').filter(id=pelajaran, kelas=kelas)
                nil = NilaiMataPelajaran.objects.values('nilai').filter(pelajaran=pelajaran, siswa=siswa)
                if not nil:
                    for pel in pel:
                        pel_nilai.append({pel['nama']: 0})
                else:
                    for pel, nil in zip(pel, nil):
                        pel_nilai.append({pel['nama']: nil['nilai']})     
        except ObjectDoesNotExist:
            kelas = None
            pel_nilai = None

        context = {
                'kelas': kelas,
                'skor' : pel_nilai,
        }

    return render(request, 'dashboard/dashboard.html', context)

class Registration(View):
    def get(self, request, level=''):
        user_form = RegistrationForm()
        level = level.lower()
        if level == 'guru' or level == 'g':
            extra_form = GuruForm()
        elif level == 'siswa' or level == 'g':
            extra_form = SiswaForm()
        else:
            raise Http404

        context = {
            'user_form' : user_form,
            'extra_form' : extra_form,
        }

        return render(request, 'registration/register.html', context)

    def post(self, request, level=''):
        user_form = RegistrationForm(request.POST)
        level = level.lower()
        if level == 'guru' or level == 'g':
            extra_form = GuruForm(request.POST)
        elif level == 'siswa' or level == 'g':
            extra_form = SiswaForm(request.POST)
        else:
            raise Http404

        if user_form.is_valid() and extra_form.is_valid():
            username = f"{level.upper()[0]}-{user_form.cleaned_data.get('nomor_induk')}-{extra_form.cleaned_data.get('nama').lower().split(' ')[0]}"
            user = user_form.save(commit=False)
            user.username = username
            user.level = level.upper()[0]
            user.save()

            if level == 'siswa' or level == 's':
                user.akun_siswa.nama = extra_form.cleaned_data.get('nama')
                user.akun_siswa.nis = extra_form.cleaned_data.get('nis')
                user.akun_siswa.tanggal_lahir = extra_form.cleaned_data.get('tanggal_lahir')
                user.akun_siswa.gender = extra_form.cleaned_data.get('gender')
                user.akun_siswa.kelas = extra_form.cleaned_data.get('kelas')
                user.akun_siswa.jurusan = extra_form.cleaned_data.get('jurusan')
                user.akun_siswa.save()

            elif level == 'guru' or level == 'g':
                user.akun_guru.nama = extra_form.cleaned_data.get('nama')
                user.akun_guru.tanggal_lahir = extra_form.cleaned_data.get('tanggal_lahir')
                user.akun_guru.gender = extra_form.cleaned_data.get('gender')
                user.akun_guru.save()

            return redirect('dashboard')
        else:
            context = {
                'user_form' : user_form,
                'extra_form' : extra_form,
            }
            return render(request, 'registration/register.html', context)