from django.contrib import admin
from User.models import User, Guru, Siswa
from User.forms import RegistrationForm, EditUserForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = EditUserForm
    add_form = RegistrationForm
    
    list_display = ('nomor_induk', 'level')
    list_filter = ('level',)
    fieldsets = (
        ('Account Profile', {'fields': ('nomor_induk', 'nama', 'password')}),
        ('Account Status', {'fields': ('is_active',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nomor_induk', 'level', 'password1', 'password2'),
        }),
    )
    search_fields = ('nomor_induk',)
    ordering = ('level',)            
    filter_horizontal = ()

@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nip', 'gender')

    fieldsets = (
        ('Profil Guru', {'fields': ('nip', 'nama', 'gender', 'tanggal_lahir')}),       
    )
    search_fields = ('nip', 'nama')
    ordering = ('nama',)
    
@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nisn', 'gender', 'kelas')
    list_filter = ('kelas', 'gender')
    fieldsets = (
        ('Profil Siswa', {'fields': ('nisn', 'nis', 'nama', 'gender', 'tanggal_lahir', 'kelas')}),        
    )
    ordering=('nama', 'kelas')

admin.site.unregister(Group)



