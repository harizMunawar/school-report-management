# Generated by Django 3.1 on 2020-09-10 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0013_auto_20200901_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siswa',
            name='nis',
        ),
    ]
