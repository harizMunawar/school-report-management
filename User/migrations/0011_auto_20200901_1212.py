# Generated by Django 3.1 on 2020-09-01 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_auto_20200901_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siswa',
            name='gender',
            field=models.CharField(choices=[('P', 'Pria'), ('W', 'Wanita')], default='P', max_length=2, null=True),
        ),
    ]
