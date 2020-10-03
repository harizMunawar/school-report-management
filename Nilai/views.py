from django.shortcuts import render, redirect
from django.views.generic import View
from Nilai.models import MataPelajaran, NilaiMataPelajaran
from Kelas.models import Kelas
from User.models import Siswa
from django.contrib.auth.decorators import login_required
from django.http import Http404
from Helpers import zip_pelnilai

class ListNilai(View):        
    def get(self, request, nisn):        
        if request.user.is_authenticated and not request.user.level == 'S':
            try:
                siswa = Siswa.objects.get(nisn=nisn)          
                kelas = Kelas.objects.get(nama=siswa.kelas)
                data = zip_pelnilai(siswa)                
                
                context = {
                    'data': data,
                }
                
                return render(request, 'nilai/form-nilai.html', context)
            except Siswa.DoesNotExist:
                raise Http404      
        else:
            return redirect('dashboard')
    
    def post(self, request, nisn):
        if request.user.is_authenticated and not request.user.level == 'S':            
            try:                
                siswa = Siswa.objects.get(nisn=nisn)
                kelas = Kelas.objects.get(nama=siswa.kelas)
                data = zip_pelnilai(siswa)
                completed = True
                for id_, pelajaran, nilai in data:
                    matapelajaran = MataPelajaran.objects.filter(id=id_)[0]
                    form_nilai = request.POST.get(f'{id_}')
                    if form_nilai == '0':
                        completed = False
                    obj, created = NilaiMataPelajaran.objects.update_or_create(
                        siswa=siswa, pelajaran=matapelajaran, 
                        defaults={'nilai': form_nilai}
                    )
                
                if completed == True:
                    return redirect(f'/export-pdf/{nisn}/?action=')
                else:
                    return redirect('dashboard')
            except Siswa.DoesNotExist: 
                raise Http404      
        else:
            return redirect('dashboard')