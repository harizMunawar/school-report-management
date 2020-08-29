from django.db import models


class MataPelajaran(models.Model):
    nama = models.CharField(max_length=50)
    kkm = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.nama

class NilaiMataPelajaran(models.Model):
    pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.PROTECT, related_name='nilai')
    siswa = models.ForeignKey("User.Siswa", on_delete=models.CASCADE, related_name='nilai_matpel')
    nilai = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.siswa} {self.pelajaran}'

class Ekskul(models.Model):
    JENIS_EKSKUL = [
        ('Kepemimpinan', 'Kepemimpinan'),
        ('Keagamaan', 'Keagamaan'),
        ('Kesenian', 'Kesenian'),
        ('Olahraga', 'Olahraga'),              
        ('Lain-Lain', 'Lain-Lain'),
    ]

    nama = models.CharField(max_length=50)
    deskripsi = models.TextField(null=True, blank=True)
    jenis = models.CharField(choices=JENIS_EKSKUL, max_length=25)
    pembimbing = models.ForeignKey("User.Guru", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nama

class NilaiEkskul(models.Model):
    NILAI_EKSKUL = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
    ]

    ekskul = models.ForeignKey(Ekskul, on_delete=models.PROTECT, related_name='nilai')
    siswa = models.ForeignKey("User.Siswa", on_delete=models.CASCADE, related_name='nilai_ekskul')
    nilai = models.CharField(choices=NILAI_EKSKUL, default=NILAI_EKSKUL[0][0], max_length=3)

    def __str__(self):
        return f'{self.siswa} {self.ekskul}'