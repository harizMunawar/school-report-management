from django.db import models

class Jurusan(models.Model):
    nama = models.CharField(max_length=50, unique=True)
    akronim = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.akronim

class MataPelajaran(models.Model):
    nama = models.CharField(max_length=50)
    kkm = models.SmallIntegerField()

    # def save(self, *args, **kwargs):
    #     if int(self.kkm) > 100:
    #         self.kkm = 100
    #         super(MataPelajaran, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama

class Kelas(models.Model):
    TINGKAT_LIST = [
        ('10', 'X'),
        ('11', 'XI'),
        ('12', 'XII')
    ]

    HURUF_LIST = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ]

    jurusan = models.ForeignKey(Jurusan, on_delete=models.PROTECT, related_name='kelas')
    tingkat = models.CharField(max_length=3, choices=TINGKAT_LIST)
    kelas = models.CharField(max_length=1, choices=HURUF_LIST)
    nama = models.CharField(max_length=15, null=True, blank=True)
    matapelajaran = models.ManyToManyField(MataPelajaran, related_name='kelas')
    walikelas = models.OneToOneField("User.Guru", on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.nama = f'{self.tingkat} {self.jurusan} {self.kelas}'
        super(Kelas, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama



