from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
import tempfile
from Nilai.views import get_unzip, get_data
from django.views.generic import View
from User.models import Siswa
from Kelas.models import Kelas

class ExportPDF(View):
    def get(self, request):
        siswa = Siswa.objects.get(nisn=request.GET['nisn'])
        kelas = Kelas.objects.get(walikelas=self.request.user.akun_guru)
        data = get_data(siswa, kelas)

        html_string = render_to_string('exports/output.html', {'data': data, 'siswa':siswa})
        html = HTML(string=html_string)
        result = html.write_pdf()#target=settings.BASE_DIR/'pdf/contoh.pdf'

        response = HttpResponse(result, content_type='application/pdf;')
        response['Content-Disposition'] = f'inline; filename={siswa.user.username}.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        
        return response
