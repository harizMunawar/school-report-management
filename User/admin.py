from django.contrib import admin
from User.models import User, Guru, Siswa
from User.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('username', 'nomor_induk', 'level')
    list_filter = ('level',)
    fieldsets = (
        ('Account Profile', {'fields': ('nomor_induk', 'password', 'username')}),
        ('Account Status', {'fields': ('is_active',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nomor_induk', 'username', 'level', 'password1', 'password2'),
        }),
    )
    search_fields = ('nomor_induk', 'username')
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Guru)
admin.site.register(Siswa)
admin.site.unregister(Group)



