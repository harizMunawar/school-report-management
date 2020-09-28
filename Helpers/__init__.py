from Nilai.models import MataPelajaran, NilaiMataPelajaran

def zip_pelnilai(siswa, kelas):    
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

def zip_siswa_status(list_siswa, kelas):
    status = []    
    for siswa in list_siswa:
        id_, pelajaran, nilai = list(zip(*zip_pelnilai(siswa, kelas)))
        if 0 in nilai: status.append(False)
        else: status.append(True)
    return zip(list_siswa, status)

def get_finished_siswa(list_siswa, kelas):
    finished = []    
    for siswa in list_siswa:
        id_, pelajaran, nilai = list(zip(*zip_pelnilai(siswa, kelas)))
        if not 0 in nilai: finished.append(siswa)        
    return finished

def get_unfinished_siswa(list_siswa, kelas):
    unfinished = []
    for siswa in list_siswa:
        id_, pelajaran, nilai = list(zip(*zip_pelnilai(siswa, kelas)))
        if 0 in nilai: unfinished.append(siswa)        
    return unfinished