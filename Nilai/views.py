from django.shortcuts import render, redirect
from django.views.generic import View
from Nilai.models import MataPelajaran, NilaiMataPelajaran
from Kelas.models import Kelas
from User.models import Siswa
from django.contrib.auth.decorators import login_required
from django.http import Http404

def get_data(siswa, kelas):    
    matapelajaran = MataPelajaran.objects.values('id', 'nama').filter(kelas=kelas)[::1]
    list_id = []
    list_pelajaran = []            
    list_nilai = []

    for pelajaran in matapelajaran:
        list_pelajaran.append(pelajaran['nama'])
        list_id.append(pelajaran['id'])
        nil = NilaiMataPelajaran.objects.values('nilai').filter(pelajaran=pelajaran['id'], siswa=siswa)
        if not nil:
            list_nilai.append(0)
        else:
            for nil in nil:
                list_nilai.append(nil['nilai'])

    return zip(list_id, list_pelajaran, list_nilai)

def get_unzip(siswa, kelas):
    data = get_data(siswa, kelas)
    res = list(zip(*data))
    return res

class ListNilai(View):        
    def get(self, request, nisn):        
        if request.user.is_authenticated and not request.user.level == 'S':
            try:
                siswa = Siswa.objects.get(nisn=nisn)
                kelas = Kelas.objects.get(walikelas=request.user.akun_guru)
                data = get_data(siswa, kelas)                
                
                context = {
                    'data': data,
                }
                
                return render(request, 'nilai/form_nilai.html', context)
            except Siswa.DoesNotExist:
                raise Http404      
        else:
            return redirect('dashboard')
    
    def post(self, request, nisn):
        if request.user.is_authenticated and not request.user.level == 'S':            
            try:                
                siswa = Siswa.objects.get(nisn=nisn)
                kelas = Kelas.objects.get(walikelas=request.user.akun_guru)
                data = get_data(siswa, kelas)
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