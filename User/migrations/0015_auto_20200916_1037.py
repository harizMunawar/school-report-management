# Generated by Django 3.1 on 2020-09-16 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_remove_siswa_nis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guru',
            name='nama',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
