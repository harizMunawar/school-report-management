from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from Helpers import zip_pelnilai
from django.views.generic import View
from User.models import Siswa
from Kelas.models import Kelas
import os
import shutil

def export_pdf(siswa, data, pdf_dir):
    if not os.path.isdir(pdf_dir): 
        os.makedirs(pdf_dir)
    
    html_string = render_to_string('rapor/pdf-output.html', {'data': data, 'siswa':siswa})
    html = HTML(string=html_string)
    html.write_pdf(target=f'{pdf_dir}/{siswa.nama}.pdf')

class ExportPDF(View):
    def get(self, request, nisn):               
        siswa = Siswa.objects.get(nisn=nisn)
        data = zip_pelnilai(siswa)
        pdf_dir = f'{settings.BASE_DIR}\media\pdf\{siswa.kelas}'
        
        export_pdf(siswa, data, pdf_dir)

        with open(f'{pdf_dir}/{siswa.nama}.pdf', 'rb') as result:            
            response = HttpResponse(result, content_type='application/pdf;')
            if request.GET['action'] == 'download':
                response['Content-Disposition'] = f'attachment; filename={siswa.nama}.pdf'
                response['Content-Transfer-Encoding'] = 'binary'
            elif request.GET['action'] == 'preview':
                response['Content-Disposition'] = f'inline; filename={siswa.nama}.pdf'
                response['Content-Transfer-Encoding'] = 'binary'
            else:
                return redirect('dashboard')
            return response

class BundleExport(View):
    def get(self, request, kelas):
        kelas = Kelas.objects.get(nama=kelas)
        pdf_dir = f'{settings.BASE_DIR}/media/pdf/{kelas}'
        bundle_dir = f'{settings.BASE_DIR}/media/bundle/{kelas.jurusan}'

        anggota_kelas = Siswa.objects.filter(kelas=kelas)

        for siswa in anggota_kelas:
            siswa = Siswa.objects.get(nisn=siswa.nisn)
            data = zip_pelnilai(siswa)

            export_pdf(siswa, data, pdf_dir)

        if not os.path.isdir(bundle_dir): 
            os.makedirs(bundle_dir)

        shutil.make_archive(f'{bundle_dir}/Rapor-{kelas}', 'zip', pdf_dir)
        zip_file = open(f'{bundle_dir}/Rapor-{kelas}.zip', 'rb')
        response = FileResponse(zip_file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename=Rapor-{kelas}.zip'

        return response
