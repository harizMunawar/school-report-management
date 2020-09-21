from django import forms
from Kelas.models import Kelas

class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas        
        fields = ('tingkat', 'jurusan', 'kelas', 'matapelajaran', 'walikelas')        