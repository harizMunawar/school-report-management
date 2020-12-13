from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
import Kelas.models
from datetime import datetime
import Helpers.choices as choice

class UserManager(BaseUserManager):
    def create_user(self, nomor_induk, level, password=None):
        if not nomor_induk or not level:
            raise ValueError("Data is not complete")        

        user = self.model(nomor_induk = nomor_induk, level = level)
        if user.level == 'A':
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True            
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nomor_induk, level, password):
        user = self.create_user(nomor_induk = nomor_induk, password = password, level = level)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):    
    nomor_induk = models.CharField(verbose_name="Nomor Induk", unique=True, max_length=18)
    level = models.CharField(choices=choice.USER_ROLE, max_length=1)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)    
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'nomor_induk'
    REQUIRED_FIELDS = ['level']

    objects = UserManager()

    def __str__(self):
        return self.nomor_induk

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Guru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='akun_guru', null=True, blank=True)
    nip = models.CharField(unique=True, max_length=18)
    nama = models.CharField(max_length=50, null=True, blank=True, default='')
    tanggal_lahir = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=2, choices=choice.GENDER_LIST, default=choice.GENDER_LIST[0][0])

    def save(self, *args, **kwargs):        
        super(Guru, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama

class Siswa(models.Model):    
    nama = models.CharField(max_length=50, null=True, blank=True, default='')
    gender = models.CharField(max_length=2, choices=choice.GENDER_LIST, default=choice.GENDER_LIST[0][0], null=True)
    nisn = models.CharField(max_length=10, unique=True)
    nis = models.CharField(max_length=10, unique=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    kelas = models.ForeignKey("Kelas.Kelas", on_delete=models.PROTECT, related_name='siswa', null=True, blank=True)    

    def save(self, *args, **kwargs):        
        super(Siswa, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama    

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and not instance.level == 'A':
#         if instance.level == 'G':
#             Guru.objects.create(user = instance)
#             akun = Guru.objects.get(user=instance)
#         else:
#             Siswa.objects.create(user = instance)
#             akun = Siswa.objects.get(user=instance)
#         # akun.nama = f"{instance.username}"
#         akun.tanggal_lahir = datetime.now()
#         akun.save()

#     elif created and instance.level == 'A':
#         instance.is_admin = True
#         instance.is_staff = True
#         instance.is_superuser = True
#         instance.save()

@receiver(post_save, sender=User)
def edit_user(sender, instance, created, **kwargs):
    if created and instance.level == 'A':
        instance.is_admin = True
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()

    if created and (instance.level == 'G' or instance.level == 'T'):
        akun_guru = Guru.objects.create(user = instance)
        akun_guru.nip = instance.nomor_induk
        akun_guru.save()

@receiver(post_save, sender=Siswa)
def edit_siswa(sender, instance, created, **kwargs):
    pass

@receiver(post_save, sender=Guru)
def edit_guru(sender, instance, created, **kwargs):
    pass