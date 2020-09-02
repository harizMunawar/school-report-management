from rest_framework import routers
from REST.viewsets import KelasViewSet, SiswaViewSet, MataPelajaranViewSet, GuruViewSet

router = routers.DefaultRouter()
router.register(r'kelas', KelasViewSet)
router.register(r'siswa', SiswaViewSet)
router.register(r'matapelajaran', MataPelajaranViewSet)
router.register(r'guru', GuruViewSet)