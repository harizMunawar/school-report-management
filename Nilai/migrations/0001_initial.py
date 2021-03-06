# Generated by Django 3.1 on 2020-08-29 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0005_auto_20200827_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ekskul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
                ('deskripsi', models.TextField(blank=True, null=True)),
                ('jenis', models.CharField(choices=[('Kepemimpinan', 'Kepemimpinan'), ('Keagamaan', 'Keagamaan'), ('Kesenian', 'Kesenian'), ('Olahraga', 'Olahraga'), ('Lain-Lain', 'Lain-Lain')], max_length=25)),
                ('pembimbing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='User.guru')),
            ],
        ),
        migrations.CreateModel(
            name='MataPelajaran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
                ('kkm', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NilaiMataPelajaran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nilai', models.PositiveSmallIntegerField()),
                ('pelajaran', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nilai', to='Nilai.matapelajaran')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nilai_matpel', to='User.siswa')),
            ],
        ),
        migrations.CreateModel(
            name='NilaiEkskul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nilai', models.CharField(choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], default='A+', max_length=3)),
                ('ekskul', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nilai', to='Nilai.ekskul')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nilai_ekskul', to='User.siswa')),
            ],
        ),
    ]
