from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from User.forms import RegistrationForm, GuruForm, SiswaForm

from User.models import User, Siswa, Guru
from Kelas.models import Jurusan, Kelas
from Nilai.models import MataPelajaran, NilaiMataPelajaran

from django.core.exceptions import ObjectDoesNotExist
from collections import Counter

class GuruRegistration(View):
    def get(self, request):        
        user_form = RegistrationForm()
        guru_form = GuruForm()

        context = {
            'user_form' : user_form,
            'guru_form' : guru_form,
        }

        return render(request, 'registration/register.html', context)

    def post(self, request):
        user_form = RegistrationForm(request.POST)
        guru_form = GuruForm(request.POST)

        if user_form.is_valid() and guru_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
        
            user.akun_guru.nama = guru_form.cleaned_data.get('nama')
            user.akun_guru.tanggal_lahir = guru_form.cleaned_data.get('tanggal_lahir')
            user.akun_guru.gender = guru_form.cleaned_data.get('gender')
            user.akun_guru.save()
                        
            nomor_induk = user_form.cleaned_data.get('nomor_induk')
            raw_password = user_form.cleaned_data.get('password1')

            account = authenticate(nomor_induk=nomor_induk, password=raw_password)
            login(request, account)
            return redirect('login')
        else:
            context = {
                'user_form' : user_form,
                'guru_form' : guru_form,
            }

            return render(request, 'registration/register.html', context)
        
class SiswaRegistration(View):
    def get(self, request):        
        user_form = RegistrationForm()
        siswa_form = SiswaForm()

        context = {
            'user_form' : user_form,
            'siswa_form' : siswa_form,
        }

        return render(request, 'registration/register.html', context)

    def post(self, request):
        user_form = RegistrationForm(request.POST)
        siswa_form = SiswaForm(request.POST)

        if user_form.is_valid() and siswa_form.is_valid():
            user = user_form.save(commit=False)
            user.save()

            user.akun_siswa.nama = siswa_form.cleaned_data.get('nama')
            user.akun_siswa.nis = siswa_form.cleaned_data.get('nis')
            user.akun_siswa.tanggal_lahir = siswa_form.cleaned_data.get('tanggal_lahir')
            user.akun_siswa.gender = siswa_form.cleaned_data.get('gender')
            user.akun_siswa.kelas = siswa_form.cleaned_data.get('kelas')
            user.akun_siswa.jurusan = siswa_form.cleaned_data.get('jurusan')
            
            user.akun_siswa.save()

            nomor_induk = user_form.cleaned_data.get('nomor_induk')
            raw_password = user_form.cleaned_data.get('password1')

            # account = authenticate(nomor_induk=nomor_induk, password=raw_password)
            # login(request, account)
            return redirect('regis_siswa')
        else:
            context = {
                'user_form' : user_form,
                'siswa_form' : siswa_form,
            }

            return render(request, 'registration/register.html', context)

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
            active_kelas = None
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
            active_kelas = None
            walikelas = None

        context = {
            'kelas': kelas,
            'walikelas': kelas.walikelas,
            'skor' : pel_nilai,
        }

    return render(request, 'dashboard/dashboard.html', context)