from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    re_path(r'^register(?:/(?P<level>[\w-]+))*/$', views.Registration.as_view(), name='registration'),
    path('bulk-insert/', views.bulk_insert, name='bulk-insert')   
]
