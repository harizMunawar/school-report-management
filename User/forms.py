from django import forms
from django.contrib.auth.forms import UserCreationForm
from User.models import User, Guru, Siswa
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistrationForm(UserCreationForm):    
    nomor_induk = forms.CharField(max_length=18)

    class Meta:
        model = User
        fields = ("nomor_induk", "password1", "password2", "level")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        
class EditUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('nomor_induk', 'level', 'password', 'is_active')

    def clean_password(self):
        return self.initial["password"]
        
class GuruForm(forms.ModelForm):
    class Meta:
        model = Guru        
        fields = ('nama', 'gender', 'tanggal_lahir')
        widgets = {
            'tanggal_lahir': DateInput()
        }

class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa        
        fields = '__all__'
        # ('nama',  'nis', 'nisn', 'gender', 'tanggal_lahir', 'kelas')
        widgets = {
            'tanggal_lahir': DateInput()
        }