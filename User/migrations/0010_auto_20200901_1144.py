# Generated by Django 3.1 on 2020-09-01 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_auto_20200901_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guru',
            name='nip',
            field=models.CharField(default='null', editable=False, max_length=18, unique=True),
        ),
    ]
