from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from User.forms import RegistrationForm, GuruForm, SiswaForm

from User.models import User, Siswa, Guru
from Kelas.models import Jurusan, Kelas

from django.core.exceptions import ObjectDoesNotExist

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
            user.akun_guru.save()
                        
            nomor_induk = user_form.cleaned_data.get('nomor_induk')
            raw_password = user_form.cleaned_data.get('password1')

            account = authenticate(nomor_induk=nomor_induk, password=raw_password)
            login(request, account)
            return redirect('dashboard')
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
            user.akun_siswa.tanggal_lahir = siswa_form.cleaned_data.get('tanggal_lahir')
            user.akun_siswa.kelas = siswa_form.cleaned_data.get('kelas')
            user.akun_siswa.jurusan = siswa_form.cleaned_data.get('jurusan')
            user.akun_siswa.save()

            nomor_induk = user_form.cleaned_data.get('nomor_induk')
            raw_password = user_form.cleaned_data.get('password1')

            account = authenticate(nomor_induk=nomor_induk, password=raw_password)
            login(request, account)
            return redirect('dashboard')
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
            active_guru = Guru.objects.get(user = active_user)
            active_kelas = Kelas.objects.get(walikelas=active_guru.id)
            list_siswa = Siswa.objects.filter(kelas = active_kelas.id)
        except ObjectDoesNotExist:
            active_kelas = None
            list_siswa = None

        context = {
            'siswa': list_siswa,
            'kelas': active_kelas,
        }

    if active_user.level == 'S':
        try:
            active_siswa = Siswa.objects.get(user = active_user)
            active_kelas = Kelas.objects.get(nama=active_siswa.kelas)
            walikelas = Guru.objects.get(nama=active_kelas.walikelas)
        except ObjectDoesNotExist:
            active_kelas = None
            walikelas = None

        context = {
            'kelas': active_kelas,
            'walikelas': walikelas,
        }


    return render(request, 'dashboard/dashboard.html', context)

