from django.shortcuts import render, redirect
from django.views.generic import View, FormView, DetailView
from django.contrib.auth.decorators import login_required
from User.forms import RegistrationForm, GuruForm, SiswaForm

from User.models import User, Siswa, Guru
from Kelas.models import Jurusan, Kelas
from Nilai.models import MataPelajaran, NilaiMataPelajaran
from Nilai.views import get_data, get_unzip

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from collections import Counter
from django.conf import settings
from django.contrib.auth import hashers
import json

@login_required
def dashboard(request):
    context = {}
    active_user = User.objects.get(nomor_induk = request.user.nomor_induk)
    if active_user.level == 'G':  
        try:      
            guru = Guru.objects.get(user=active_user)
            kelas = Kelas.objects.get(walikelas=guru.id)
            list_siswa = Siswa.objects.filter(kelas=kelas.id).order_by('nama')
            status = []
            bundle_export = True
            for siswa in list_siswa:
                id_, pelajaran, nilai = get_unzip(siswa, kelas)
                if 0 in nilai:
                    status.append(False)
                else:
                    status.append(True)

            if False in status:
                bundle_export = False              
                   
        except ObjectDoesNotExist:
            kelas = None
            list_siswa = None

        context = {
            'siswa': list_siswa,
            'kelas': kelas,
            'data': zip(list_siswa, status),
            'bundle_export': bundle_export,
        }

    if active_user.level == 'S':
        try:
            siswa = Siswa.objects.get(user=active_user)
            kelas = Kelas.objects.get(nama=siswa.kelas)
            matapelajaran = MataPelajaran.objects.values('id', 'nama').filter(kelas=kelas)[::1]                        
            data = get_data(siswa, kelas)
        except ObjectDoesNotExist:
            kelas = None
            data = None            
        context = {
                'kelas': kelas,
                'data' : data,
        }

    if active_user.level == 'A':        
        siswa = Siswa.objects.all()                    
        context = {
                'siswa': siswa,                
        }

    return render(request, 'user/dashboard/dashboard.html', context)

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

        return render(request, 'user/registration/register.html', context)

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
            user = user_form.save(commit=False)            
            user.username = f"{level.upper()[0]}-{extra_form.cleaned_data.get('nama').title().split(' ')[-1]}-{user_form.cleaned_data.get('nomor_induk')}"
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
            return render(request, 'user/registration/register.html', context)

class EditSiswa(DetailView):    
    model = Siswa
    template_name = 'user/siswa/detail-siswa.html'
    slug_field = 'nisn'
    slug_url_kwarg = 'nisn'

    def post(self, request, nisn):
        nama = request.POST['nama']
        gender = request.POST['gender'][0]
        nisn = request.POST['nisn']
        tanggal_lahir = request.POST['tanggal_lahir']
        kelas = Kelas.objects.get(nama=request.POST['kelas'])

        Siswa.objects.update_or_create(
            nisn=nisn,
            defaults={
                'nama': nama,
                'gender': gender,
                'nisn': nisn,
                'tanggal_lahir': tanggal_lahir,
                'kelas': kelas,
                },
        )
        return redirect('dashboard')



def bulk_insert(request):
    f = open(settings.BASE_DIR/'student.json')
    data = json.load(f)
    pointer = 0
    for data in data:
        if data['Akronim'] == 'RPL':
            username = f"S-{data['Nama'].title().split(' ')[-1]}-{data['NISN']}"
            password = hashers.make_password(data['NISN'])
            account = User.objects.create(nomor_induk=data['NISN'], level='S', username=username, password=password)
            obj, created = Siswa.objects.update_or_create(
                user=account, nisn=data['NISN'],
                defaults={'nama': data['Nama']},
            )
            pointer += 1
            if pointer % 10 == 0:
                print(f'Total {pointer} rows of data has been inserted successfully')
    f.close()
    return render(request, 'user/dashboard/dashboard.html')
