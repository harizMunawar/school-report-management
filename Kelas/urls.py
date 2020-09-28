from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ListKelas.as_view(), name="list-kelas"),
    path('<nama>/', include([
        path('', views.DetailKelas.as_view(), name='detail-kelas'),
        path('edit/', views.EditKelas.as_view(), name="edit-kelas"),
        path('delete/', views.DeleteKelas.as_view(), name="delete-kelas"),
    ])),    
    path('create/', views.CreateKelas.as_view(), name="create-kelas"),    
]
