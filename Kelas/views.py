from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from Kelas.models import Kelas
from Kelas.forms import KelasForm
from User.models import Siswa
from Nilai.models import MataPelajaran

class DetailKelas(DetailView):
    model = Kelas
    slug_field = 'nama'
    slug_url_kwarg = 'nama'
    context_object_name = 'kelas'
    template_name = 'kelas/detail-kelas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_siswa'] =  Siswa.objects.filter(kelas=kwargs['object']).count()
        context['list_matapelajaran'] = MataPelajaran.objects.filter(kelas=kwargs['object'])
        return context

class CreateKelas(CreateView):
    model = Kelas
    template_name = 'kelas/edit-kelas.html'
    form_class = KelasForm
    success_url = '/'

class ListKelas(ListView):
    model = Kelas
    paginate_by = 5
    template_name = 'kelas/list-kelas.html'

class EditKelas(UpdateView):
    model = Kelas
    template_name = 'kelas/edit-kelas.html'
    form_class = KelasForm
    slug_field = 'nama'
    slug_url_kwarg = 'nama'
    success_url = '/'

class DeleteKelas(DeleteView):
    model = Kelas
    template_name = 'kelas/delete-kelas.html'
    slug_field = 'nama'
    slug_url_kwarg = 'nama'
    success_url = '/'