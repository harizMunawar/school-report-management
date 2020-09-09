from django.urls import path
from . import views

urlpatterns = [
    path('export-pdf/', views.ExportPDF.as_view(), name="export-pdf"),    
]