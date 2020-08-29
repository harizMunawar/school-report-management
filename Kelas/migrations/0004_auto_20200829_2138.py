# Generated by Django 3.1 on 2020-08-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kelas', '0003_delete_matapelajaran'),
        ('Nilai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kelas',
            name='matapelajaran',
            field=models.ManyToManyField(related_name='kelas', to='Nilai.MataPelajaran'),
        ),
        migrations.AlterField(
            model_name='kelas',
            name='tingkat',
            field=models.CharField(choices=[('10', 'X'), ('11', 'XI'), ('12', 'XII'), ('13', 'XIII')], max_length=3),
        ),
    ]
