from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('register/<level>/', views.Registration.as_view(), name='registration'),
    path('create/<level>/', views.CreateUser.as_view(), name='create-user'),
    path('delete/user/<nomor_induk>/', views.DeleteUser.as_view(), name='delete-user'),

    path('siswa/', views.ListSiswa.as_view(), name='list-siswa'),
    path('siswa/<nomor_induk>/', views.EditSiswa.as_view(), name='siswa'),

    path('guru/', views.ListGuru.as_view(), name='list-guru'),
    path('guru/<nomor_induk>/', views.EditGuru.as_view(), name='guru'),

    path('bulk-insert/', views.bulk_insert, name='bulk-insert'),
]
