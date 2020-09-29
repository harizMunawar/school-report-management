from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^export-pdf(?:/(?P<nisn>[\w-]+))*/$', views.ExportPDF.as_view(), name="export-pdf"),
    path('bundle-export/<kelas>', views.BundleExport.as_view(), name="bundle-export")
]