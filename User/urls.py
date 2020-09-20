from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    re_path(r'^register(?:/(?P<level>[\w-]+))*/$', views.Registration.as_view(), name='registration'),        
    path('create/<level>/', views.CreateUser.as_view(), name='create-user'),
    re_path(r'^delete/user/(?P<nomor_induk>[\w-]+)/$', views.DeleteUser.as_view(), name='delete-user'),

    path('siswa/', views.ListSiswa.as_view(), name='list-siswa'),
    re_path(r'^siswa/(?P<nomor_induk>[\w-]+)/$', views.EditSiswa.as_view(), name='siswa'),

    path('guru/', views.ListGuru.as_view(), name='list-guru'),
    re_path(r'^guru/(?P<nomor_induk>[\w-]+)/$', views.EditGuru.as_view(), name='guru'),

    path('bulk-insert/', views.bulk_insert, name='bulk-insert'),
]
