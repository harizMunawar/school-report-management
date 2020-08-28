from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('register/guru', views.GuruRegistration.as_view(), name='regis_guru'),
    path('register/siswa', views.SiswaRegistration.as_view(), name='regis_siswa'),
]
