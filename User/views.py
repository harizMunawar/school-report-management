from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import View, FormView, DetailView, UpdateView, CreateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from User.forms import RegistrationForm, GuruForm, SiswaForm, EditUserForm
from django.contrib.auth.views import PasswordChangeView, redirect_to_login
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from User.models import User, Siswa, Guru
from Kelas.models import Jurusan, Kelas
from Nilai.models import MataPelajaran, NilaiMataPelajaran

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings
from django.contrib.auth import hashers
from Helpers import zip_pelnilai, get_finished_siswa, get_unfinished_siswa, get_status, zip_siswa_status
import json
from django.db.models import Q

@login_required
def dashboard(request):
    active_user = User.objects.get(nomor_induk = request.user.nomor_induk)
    if active_user.level == 'G' or active_user.level == 'T':  
        return redirect(reverse('detail-guru', args=[active_user.nomor_induk]))

    if active_user.level == 'T':
        return render(request, 'user/dashboard/dashboard.html')

    if active_user.level == 'A':
        return render(request, 'user/dashboard/dashboard.html')

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

class CreateSiswa(View):
    def post(self, request):
        siswa_form = SiswaForm(request.POST)

        if siswa_form.is_valid():
            siswa = siswa_form.save()

            return redirect('/admin')
        else:
            context = {
                'siswa_form': siswa_form,                
            }
            return render(request, 'user/siswa/create-siswa.html', context)

    def get(self, request):
        context = {
            'siswa_form': SiswaForm(),
        }
        return render(request, 'user/siswa/create-siswa.html', context)

class DetailSiswa(DetailView):
    model = Siswa
    template_name = 'user/siswa/detail-siswa.html'
    slug_field = 'nisn'
    slug_url_kwarg = 'nisn'

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
    slug_url_kwarg = 'nisn'
    success_url = '/'

class ListSiswa(ListView):
    paginate_by = 10
    template_name = 'user/siswa/list-siswa.html'

    def get_queryset(self):
        search = False
        try:
            if 'search' in self.request.GET and self.request.GET['search'] != '':
                return Siswa.objects.filter(
                    Q(nama__icontains=self.request.GET['search']) | 
                    Q(nisn__istartswith=self.request.GET['search']) |
                    Q(kelas__nama__icontains=self.request.GET['search']))
            else:            
                return Siswa.objects.all().order_by('-kelas', 'nama')
        except ObjectDoesNotExist:
            raise Http404

class DeleteSiswa(DeleteView):
    model = Siswa
    template_name = 'user/siswa/delete-siswa.html'
    slug_field = 'nisn'
    slug_url_kwarg = 'nisn'
    success_url = '/'

class CreateGuru(View):
    def post(self, request):
        user_form = RegistrationForm(request.POST)
        guru_form = GuruForm(request.POST)

        if user_form.is_valid() and guru_form.is_valid():
            user = user_form.save()
            guru = guru_form.save(commit=False)
            guru.user = user
            guru.save()

            return redirect('/admin')
        else:
            context = {
                'user_form': user_form,
                'guru_form': guru_form
            }
            return render(request, 'user/guru/create-guru.html', context)

    def get(self, request):
        context = {
            'user_form': RegistrationForm(),
            'guru_form': GuruForm()
        }
        return render(request, 'user/guru/create-guru.html', context)

class DetailGuru(DetailView):
    model = Guru
    template_name = 'user/guru/detail-guru.html'
    slug_field = 'nip'
    slug_url_kwarg = 'nip'
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
    slug_url_kwarg = 'nip'
    success_url = '/'

class ListGuru(ListView):
    queryset = Guru.objects.all().order_by('-kelas', 'nama')
    paginate_by = 10
    template_name = 'user/guru/list-guru.html'

    def get_queryset(self):        
        try:            
            if 'search' in self.request.GET and self.request.GET['search'] != '':
                return Guru.objects.filter(
                    Q(nama__icontains=self.request.GET['search']) | 
                    Q(nip__istartswith=self.request.GET['search']) |
                    Q(kelas__nama__icontains=self.request.GET['search']))
            else:
                return Guru.objects.all().order_by('nama')
        except ObjectDoesNotExist:
            raise Http404

class DeleteGuru(DeleteView):
    model = Guru
    template_name = 'user/guru/delete-guru.html'
    slug_field = 'nip'
    slug_url_kwarg = 'nip'
    success_url = '/'

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

@method_decorator(login_required, name='dispatch')
class DGListSiswa(View):
    def get(self, request):
        list_siswa = []
        logged_guru = Guru.objects.get(nip=request.user.akun_guru.nip)
        if logged_guru.user.level == 'G':
            if logged_guru.kelas:
                if 'search' in request.GET and request.GET['search'] != '':
                    list_siswa = Siswa.objects.filter(
                            Q(kelas=request.user.akun_guru.kelas) &
                            (
                                Q(nama__icontains=request.GET['search']) | 
                                Q(nisn__istartswith=request.GET['search'])
                            )
                        ).order_by('nama')
                else:
                    list_siswa = Siswa.objects.filter(kelas=request.user.akun_guru.kelas).order_by('nama')
            else:
                list_siswa = Siswa.objects.none()
        else:
            return redirect(reverse('dashboard'))

        paginator = Paginator(list_siswa, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'siswa_status': zip(page_obj, get_status(list_siswa)),
            'page_obj': page_obj,
        }

        return render(request, 'dashboard/guru/list-siswa.html', context)

@method_decorator(login_required, name='dispatch')
class DGStatusKelas(View):
    def get(self, request):
        logged_guru = Guru.objects.get(nip=request.user.akun_guru.nip)        

        if logged_guru.user.level == 'G':
            if logged_guru.kelas:
                kelas = Kelas.objects.get(walikelas=logged_guru)
                list_siswa = Siswa.objects.filter(kelas=kelas).order_by('nama')
                context = {
                    'kelas': kelas,
                    'list_matapelajaran': MataPelajaran.objects.filter(kelas=kelas),
                    'count_siswa': Siswa.objects.filter(kelas=kelas).count(),
                    'siswa_finished': get_finished_siswa(list_siswa),
                    'siswa_unfinished': get_unfinished_siswa(list_siswa)
                }

                return render(request, 'dashboard/guru/status-kelas.html', context)
            else:
                return render(request, 'dashboard/kelas-not-found.html')
        else:
            return redirect(reverse('dashboard'))