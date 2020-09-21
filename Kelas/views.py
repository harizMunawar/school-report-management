from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from Kelas.models import Kelas
from Kelas.forms import KelasForm

class CreateKelas(CreateView):
    model = Kelas
    template_name = 'kelas/detail-kelas.html'
    form_class = KelasForm
    success_url = '/'

class ListKelas(ListView):
    model = Kelas
    paginate_by = 5
    template_name = 'kelas/list-kelas.html'

class EditKelas(UpdateView):
    model = Kelas
    template_name = 'kelas/detail-kelas.html'
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