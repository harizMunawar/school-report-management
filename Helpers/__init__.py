from Nilai.models import MataPelajaran, NilaiMataPelajaran

def zip_pelnilai(siswa):        
    matapelajaran = MataPelajaran.objects.values('id', 'nama').filter(kelas=siswa.kelas)[::1]
    list_id = [pelajaran['id'] for pelajaran in matapelajaran]
    list_pelajaran = [pelajaran['nama'] for pelajaran in matapelajaran]            
    list_nilai = []

    for pelajaran in matapelajaran:
        nil = NilaiMataPelajaran.objects.values('nilai').filter(pelajaran=pelajaran['id'], siswa=siswa)
        if not nil:
            list_nilai.append(0)
        else:
            for nil in nil:
                list_nilai.append(nil['nilai'])

    return zip(list_id, list_pelajaran, list_nilai)

def get_nilai(siswa):
    matapelajaran = MataPelajaran.objects.values('id').filter(kelas=siswa.kelas)[::1]
    list_nilai = []
    
    for pelajaran in matapelajaran:
        nil = NilaiMataPelajaran.objects.values('nilai').filter(pelajaran=pelajaran['id'], siswa=siswa)
        if not nil:
            list_nilai.append(0)
        else:
            for nil in nil:
                list_nilai.append(nil['nilai'])
    return list_nilai    

def zip_siswa_status(list_siswa):    
    return [(siswa, False) if 0 in get_nilai(siswa) else (siswa, True) for siswa in list_siswa]    

def get_finished_siswa(list_siswa):
    return [siswa for siswa in list_siswa if not 0 in get_nilai(siswa)]

def get_unfinished_siswa(list_siswa):
    return [siswa for siswa in list_siswa if 0 in get_nilai(siswa)]
