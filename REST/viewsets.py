from rest_framework import permissions
from rest_framework import viewsets
from User.models import Siswa, Guru
from Kelas.models import Kelas
from Nilai.models import MataPelajaran, NilaiMataPelajaran, Ekskul, NilaiEkskul
from REST.serializers import KelasSerializers, SiswaSerializers, MataPelajaranSerializers, GuruSerializers, NilaiMataPelajaranSerializers

class KelasViewSet(viewsets.ModelViewSet):
    queryset = Kelas.objects.all().order_by('jurusan')
    serializer_class = KelasSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SiswaViewSet(viewsets.ModelViewSet):
    queryset = Siswa.objects.all().order_by('nama')
    serializer_class = SiswaSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MataPelajaranViewSet(viewsets.ModelViewSet):
    queryset = MataPelajaran.objects.all().order_by('nama')
    serializer_class = MataPelajaranSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GuruViewSet(viewsets.ModelViewSet):
    queryset = Guru.objects.all().order_by('nama')
    serializer_class = GuruSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NilaiMataPelajaranViewSet(viewsets.ModelViewSet):
    queryset = NilaiMataPelajaran.objects.all()
    serializer_class = NilaiMataPelajaranSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

