from django.contrib import admin
from User.models import User, Guru, Siswa
from User.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_reverse_admin import ReverseModelAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('nomor_induk', 'level')
    list_filter = ('level',)
    fieldsets = (
        ('Account Profile', {'fields': ('nomor_induk', 'password')}),
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
    readonly_fields = ('nip',)
    search_fields = ('nip', 'nama')
    
@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nisn', 'nis', 'gender', 'kelas')
    fieldsets = (
        ('Profil Siswa', {'fields': ('user', 'nis', 'nama', 'gender', 'tanggal_lahir', 'kelas')}),        
    )
    readonly_fields = ('nisn',)

admin.site.unregister(Group)



