# Generated by Django 3.1 on 2020-08-27 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Kelas', '0002_kelas_walikelas'),
        ('User', '0003_auto_20200827_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siswa',
            name='kelas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='siswa', to='Kelas.kelas'),
        ),
    ]
