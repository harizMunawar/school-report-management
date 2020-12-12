from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    
    # Dashboard Guru (DG Stands for Dashboard Guru. Means each accesible page from dashboard when you logged in as a Guru)
    path('list-siswa/', views.DGListSiswa.as_view(), name="dg-list-siswa"),
    path('status-kelas/', views.DGStatusKelas.as_view(), name="dg-status-kelas"),
    path('edit-profil/', views.DGEditProfil.as_view(), name="dg-edit-profil"),
    
    path('user/', include([
        path('edit/<nomor_induk>/', views.EditUser.as_view(), name='edit-user'),             
        path('edit/password/<nomor_induk>/', views.EditPassword.as_view(), name='edit-password'),
        path('delete/<nomor_induk>/', views.DeleteUser.as_view(), name='delete-user'),
        path('siswa/', include([
            path('', views.ListSiswa.as_view(), name='list-siswa'),
            path('create/', views.CreateSiswa.as_view(), name='create-siswa'),
            path('<nisn>/', views.DetailSiswa.as_view(), name='detail-siswa'),
            path('<nisn>/edit', views.EditSiswa.as_view(), name='edit-siswa'),
            path('<nisn>/delete', views.DeleteSiswa.as_view(), name='delete-siswa'),
        ])),
        path('guru/', include([
            path('', views.ListGuru.as_view(), name='list-guru'),
            path('create/', views.CreateGuru.as_view(), name='create-guru'),
            path('<nip>/', views.DetailGuru.as_view(), name='detail-guru'),
            path('<nip>/edit', views.EditGuru.as_view(), name='edit-guru'),
            path('<nip>/delete', views.DeleteGuru.as_view(), name='delete-guru'),
        ])),
    ])),                          
    path('bulk-insert/', views.bulk_insert, name='bulk-insert'),
]
