# Generated by Django 3.1 on 2020-09-01 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_auto_20200901_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siswa',
            name='nis',
            field=models.CharField(default='null', max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name='siswa',
            name='nisn',
            field=models.CharField(editable=False, max_length=10, unique=True),
        ),
    ]
