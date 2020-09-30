from Nilai.models import MataPelajaran, NilaiMataPelajaran

def zip_pelnilai(siswa, kelas):    
    get_nilai(siswa, kelas)
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

def get_nilai(siswa, kelas):
    matapelajaran = MataPelajaran.objects.values('id').filter(kelas=kelas)[::1]
    list_nilai = []
    
    for pelajaran in matapelajaran:
        nil = NilaiMataPelajaran.objects.values('nilai').filter(pelajaran=pelajaran['id'], siswa=siswa)
        if not nil:
            list_nilai.append(0)
        else:
            for nil in nil:
                list_nilai.append(nil['nilai'])
    return list_nilai    

def zip_siswa_status(list_siswa, kelas):    
    return [(siswa, False) if 0 in get_nilai(siswa, siswa.kelas) else (siswa, True) for siswa in list_siswa]    

def get_finished_siswa(list_siswa):
    return [siswa for siswa in list_siswa if not 0 in get_nilai(siswa, siswa.kelas)]

def get_unfinished_siswa(list_siswa):
    return [siswa for siswa in list_siswa if 0 in get_nilai(siswa, siswa.kelas)]
