from django.urls import path, re_path
from . import views

urlpatterns = [
    # re_path(r'^nilai(?:/(?P<siswa>[\w-]+))*/$', views.ListNilai.as_view(), name='list_nilai'),
    re_path(r'^nilai/', views.ListNilai.as_view(), name='list_nilai')
]
