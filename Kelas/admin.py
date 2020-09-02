from django.contrib import admin
from django.db.models import Count
from Kelas.models import Kelas, Jurusan
from User.models import Siswa

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Deskripsi Kelas', {'fields': ('tingkat', 'jurusan', 'kelas')}),
        ('Walikelas', {'fields': ('walikelas',)}),
        ('Mata Pelajaran Yang Ada Di Kelas', {'fields': ('matapelajaran',)}),
    )
    ordering = ('jurusan',)
    list_display = ('nama', 'walikelas')
    list_filter = ('tingkat', 'jurusan')
    search_fields = ('tingkat', 'jurusan', 'nama', 'walikelas')

admin.site.register(Jurusan)
