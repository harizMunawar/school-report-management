from Nilai.models import MataPelajaran, NilaiMataPelajaran

def nilai(id, siswa):
    nil = NilaiMataPelajaran.objects.values('nilai').filter(pelajaran=id, siswa=siswa)
    if nil:
        for nil in nil:
            return nil['nilai']
    else:
        return 0    

def zip_pelnilai(siswa):        
    matapelajaran = MataPelajaran.objects.values('id', 'nama').filter(kelas=siswa.kelas)[::1]
    list_id = [pelajaran['id'] for pelajaran in matapelajaran]
    list_pelajaran = [pelajaran['nama'] for pelajaran in matapelajaran]            
    list_nilai = [nilai(pelajaran['id'], siswa) for pelajaran in matapelajaran]

    return zip(list_id, list_pelajaran, list_nilai)

def get_nilai(siswa):
    matapelajaran = MataPelajaran.objects.values('id').filter(kelas=siswa.kelas)[::1]
   
    return [nilai(pelajaran['id'], siswa) for pelajaran in matapelajaran]   

def zip_siswa_status(list_siswa):    
    return [(siswa, False) if 0 in get_nilai(siswa) else (siswa, True) for siswa in list_siswa]    

def get_finished_siswa(list_siswa):
    return [siswa for siswa in list_siswa if not 0 in get_nilai(siswa)]

def get_unfinished_siswa(list_siswa):
    return [siswa for siswa in list_siswa if 0 in get_nilai(siswa)]
