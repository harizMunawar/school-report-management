# Generated by Django 3.1 on 2020-09-01 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20200831_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='guru',
            name='gender',
            field=models.CharField(choices=[('P', 'Pria'), ('W', 'Wanita')], default='P', max_length=2),
        ),
        migrations.AddField(
            model_name='guru',
            name='nip',
            field=models.CharField(default='null', editable=False, max_length=18, unique=True),
        ),
        migrations.AddField(
            model_name='siswa',
            name='gender',
            field=models.CharField(choices=[('P', 'Pria'), ('W', 'Wanita')], default='P', max_length=2),
        ),
    ]