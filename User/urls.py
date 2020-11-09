from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),        
    path('user/', include([
        path('register/<level>/', views.Registration.as_view(), name='registration'),
        path('create/<level>/', views.CreateUser.as_view(), name='create-user'),
        path('edit/<nomor_induk>/', views.EditUser.as_view(), name='edit-user'),             
        path('edit/password/<nomor_induk>/', views.EditPassword.as_view(), name='edit-password'),
        path('delete/<nomor_induk>/', views.DeleteUser.as_view(), name='delete-user'),
        path('siswa/', include([
            path('', views.ListSiswa.as_view(), name='list-siswa'),
            path('kelas/<kelas>', views.ListSiswa_Kelas.as_view(), name='list-siswa-kelas'),
            path('<nomor_induk>/', views.DetailSiswa.as_view(), name='detail-siswa'),
            path('<nomor_induk>/edit', views.EditSiswa.as_view(), name='edit-siswa'),
            # path('<nomor_induk>/delete', views.DeleteSiswa.as_view(), name='delete-siswa'),
        ])),
        path('guru/', include([
            path('', views.ListGuru.as_view(), name='list-guru'),        
            path('<nomor_induk>/', views.DetailGuru.as_view(), name='detail-guru'),
            path('<nomor_induk>/edit', views.EditGuru.as_view(), name='edit-guru'),
            # path('<nomor_induk>/delete', views.DeleteGuru.as_view(), name='delete-guru'),
        ])),  
    ])),                  
    path('bulk-insert/', views.bulk_insert, name='bulk-insert'),
]
