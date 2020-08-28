from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
import Kelas.models
from datetime import datetime

class UserManager(BaseUserManager):
    def create_user(self, nomor_induk, level, username, password=None):
        if not nomor_induk or not level or not username:
            raise ValueError("Data is not complete")
        
        user = self.model(nomor_induk = nomor_induk, level = level, username = username,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nomor_induk, level, username, password):
        user = self.create_user(nomor_induk = nomor_induk, password = password, level = level, username = username)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    USER_ROLE = [
        ('A','Admin'),
        ('G','Guru'),
        ('S','Siswa')
    ]

    nomor_induk = models.CharField(verbose_name="Nomor Induk", unique=True, max_length=18)
    level = models.CharField(choices=USER_ROLE, max_length=1)
    username = models.CharField(max_length=10)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)    
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'nomor_induk'
    REQUIRED_FIELDS = ['level', 'username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Guru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='akun_guru', null=True, blank=True)
    nama = models.CharField(max_length=50, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nama

class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='akun_siswa', null=True, blank=True) 
    nama = models.CharField(max_length=50, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    kelas = models.ForeignKey("Kelas.Kelas", on_delete=models.PROTECT, related_name='siswa', null=True, blank=True)    

    def __str__(self):
        return self.nama

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.level == 'A':
        if instance.level == 'G':
            Guru.objects.create(user = instance)
            akun = Guru.objects.get(user=instance)
        elif instance.level == 'S':
            Siswa.objects.create(user = instance)
            akun = Siswa.objects.get(user=instance)
        akun.nama = f"{instance.username}"
        akun.tanggal_lahir = datetime.now()
        akun.save()

    elif created and instance.level == 'A':
        instance.is_admin = True
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()        

        