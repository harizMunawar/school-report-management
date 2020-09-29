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

class ExportPDF(View):
    def get(self, request, nisn):        
        siswa = Siswa.objects.get(nisn=nisn)
        data = zip_pelnilai(siswa, siswa.kelas)
        pdf_dir = f'{settings.BASE_DIR}\media\pdf\{siswa.kelas}'

        if not os.path.isdir(pdf_dir): 
            os.makedirs(pdf_dir)

        html_string = render_to_string('rapor/pdf-output.html', {'data': data, 'siswa':siswa})
        html = HTML(string=html_string)
        result = html.write_pdf(target=f'{pdf_dir}/{siswa.nama}.pdf')

        with open(f'{pdf_dir}/{siswa.nama}.pdf', 'rb') as result:            
            response = HttpResponse(result, content_type='application/pdf;')
            if request.GET['action'] == 'download':
                response['Content-Disposition'] = f'attachment; filename={siswa.nama}.pdf'
                response['Content-Transfer-Encoding'] = 'binary'
            elif request.GET['action'] == 'preview':
                response['Content-Disposition'] = f'inline; filename={siswa.nama}.pdf'
                response['Content-Transfer-Encoding'] = 'binary'
                # context = {'path': f'{settings.MEDIA_URL}pdf/{siswa.kelas}/{siswa.nama}.pdf'}
                # return render(request, 'rapor/preview.html', context)
            else:
                return redirect('dashboard')
            return response

class BundleExport(View):
    def get(self, request, kelas):
        kelas = Kelas.objects.get(nama=kelas)
        pdf_dir = f'{settings.BASE_DIR}/media/pdf/{kelas}'
        bundle_dir = f'{settings.BASE_DIR}/media/bundle'
        zip_file = shutil.make_archive(f'{bundle_dir}/Rapor-{kelas}', 'zip', pdf_dir)
        
        zip_file = open(f'{bundle_dir}/Rapor-{kelas}.zip', 'rb')
        response = FileResponse(zip_file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename=Rapor-{kelas}.zip'
        return response
