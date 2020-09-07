from django import forms
from Nilai.models import NilaiMataPelajaran

class NilaiForm(forms.ModelForm):

    class Meta:
        model = NilaiMataPelajaran
        exclude = ['siswa', 'pelajaran']