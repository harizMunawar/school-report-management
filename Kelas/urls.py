from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListKelas.as_view(), name="list-kelas"),
    path('<nama>/edit/', views.EditKelas.as_view(), name="edit-kelas"),
    path('create/', views.CreateKelas.as_view(), name="create-kelas"),
    path('<nama>/delete/', views.DeleteKelas.as_view(), name="delete-kelas"),
]
