from rest_framework import serializers
from User.models import Siswa, Guru
from Kelas.models import Kelas
from Nilai.models import MataPelajaran, NilaiMataPelajaran, Ekskul, NilaiEkskul

class MataPelajaranSerializers(serializers.ModelSerializer):
    class Meta:
        model = MataPelajaran
        fields = ['nama',]

class NilaiMataPelajaranSerializers(serializers.ModelSerializer):
    pelajaran = MataPelajaranSerializers(required=True)
    class Meta:
        model = NilaiMataPelajaran
        fields = ['pelajaran', 'nilai']

class GuruSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guru
        fields = ['nama', 'nip', 'tanggal_lahir', 'gender']

class KelasSerializers(serializers.ModelSerializer):
    walikelas = GuruSerializers(required=True)
    class Meta:
        model = Kelas
        fields = ['nama', 'walikelas']

class SiswaSerializers(serializers.ModelSerializer):
    kelas = KelasSerializers(required=True)
    class Meta:
        model = Siswa
        fields = ['nama', 'nis', 'nisn', 'tanggal_lahir', 'gender', 'kelas']

