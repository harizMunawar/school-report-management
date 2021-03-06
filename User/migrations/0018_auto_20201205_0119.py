# Generated by Django 3.1 on 2020-12-04 18:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0017_guru_tu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guru',
            name='tu',
        ),
        migrations.RemoveField(
            model_name='siswa',
            name='user',
        ),
        migrations.AddField(
            model_name='siswa',
            name='nis',
            field=models.CharField(default=django.utils.timezone.now, max_length=10, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='siswa',
            name='nisn',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.CharField(choices=[('A', 'Admin'), ('G', 'Guru'), ('T', 'Staf TU'), ('S', 'Siswa')], max_length=1),
        ),
    ]
