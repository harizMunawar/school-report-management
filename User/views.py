from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import View, FormView, DetailView, UpdateView, CreateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from User.forms import RegistrationForm, GuruForm, SiswaForm, EditUserForm
from django.contrib.auth.views import PasswordChangeView

from User.models import User, Siswa, Guru
from Kelas.models import Jurusan, Kelas
from Nilai.models import MataPelajaran, NilaiMataPelajaran

from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.http import Http404
from collections import Counter
from django.conf import settings
from django.contrib.auth import hashers
from Helpers import zip_pelnilai, get_finished_siswa, get_unfinished_siswa
import json

@login_required
def dashboard(request):
    active_user = User.objects.get(nomor_induk = request.user.nomor_induk)
    if active_user.level == 'G':  
        return redirect(reverse('detail-guru', args=[active_user.nomor_induk]))

    if active_user.level == 'S':
        return redirect(reverse('detail-siswa', args=[active_user.nomor_induk]))

    if active_user.level == 'A':
        return render(request, 'user/dashboard/dashboard.html')

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

class CreateUser(CreateView):
    model = User
    template_name = 'user/dashboard/create-user.html'
    form_class = RegistrationForm
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.kwargs['level'] == 'siswa':
            obj.level = 'S'
            obj.save()
            return redirect(f'/user/siswa/{obj.nomor_induk}/edit')
        elif self.kwargs['level'] == 'guru':
            obj.level = 'G'
            obj.save()
            return redirect(f'/user/guru/{obj.nomor_induk}/edit')
            
class EditUser(UpdateView):
    model = User
    template_name = 'user/dashboard/edit-user.html'
    form_class = EditUserForm
    slug_field = 'nomor_induk'
    slug_url_kwarg = 'nomor_induk'
    success_url = '/'

class EditPassword(PasswordChangeView):
    template_name = 'user/dashboard/edit-password.html'
    success_url = '/'

class DeleteUser(DeleteView):
    model = User
    template_name = 'user/dashboard/delete-user.html'
    slug_field = 'nomor_induk'
    slug_url_kwarg = 'nomor_induk'
    success_url = '/'

class DetailSiswa(DetailView):
    model = Siswa
    template_name = 'user/siswa/detail-siswa.html'
    slug_field = 'nisn'
    slug_url_kwarg = 'nomor_induk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:            
            context['data_nilai'] = zip_pelnilai(kwargs['object'])
        except ObjectDoesNotExist:
            pass
        
        return context

class EditSiswa(UpdateView):    
    model = Siswa
    template_name = 'user/siswa/edit-siswa.html'
    form_class = SiswaForm
    slug_field = 'nisn'
    slug_url_kwarg = 'nomor_induk'
    success_url = '/'

class ListSiswa(ListView):
    paginate_by = 10
    template_name = 'user/siswa/list-siswa.html'

    def get_queryset(self):
        try:
            if not 'kelas' in self.request.GET or self.request.GET['kelas'] == '':
                return Siswa.objects.all().order_by('-kelas', 'nama')
            else:
                kelas = Kelas.objects.get(nama=self.request.GET.get('kelas', ''))
                return Siswa.objects.filter(kelas=kelas).order_by('-kelas', 'nama')
        except ObjectDoesNotExist:
            raise Http404

class DetailGuru(DetailView):
    model = Guru
    template_name = 'user/guru/detail-guru.html'
    slug_field = 'nip'
    slug_url_kwarg = 'nomor_induk'
    context_object_name = 'guru'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:   
            context['kelas'] = Kelas.objects.get(walikelas=kwargs['object'])            
            context['list_siswa'] = Siswa.objects.filter(kelas=context['kelas'])
            context['count_siswa'] = context['list_siswa'].count()
            context['finished_siswa'] = get_finished_siswa(context['list_siswa'])
            context['unfinished_siswa'] = get_unfinished_siswa(context['list_siswa'])            
        except ObjectDoesNotExist:
            pass
        return context
    
class EditGuru(UpdateView):    
    model = Guru
    template_name = 'user/guru/edit-guru.html'
    form_class = GuruForm
    slug_field = 'nip'
    slug_url_kwarg = 'nomor_induk'
    success_url = '/'

class ListGuru(ListView):
    queryset = Guru.objects.all().order_by('-kelas', 'nama')
    paginate_by = 10
    template_name = 'user/guru/list-guru.html'

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
