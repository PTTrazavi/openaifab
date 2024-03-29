# Generated by Django 2.2.4 on 2020-01-06 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_auto_20200106_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_app', models.DateField(blank=True, null=True)),
                ('work', models.TextField()),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('date_b0', models.DateField(blank=True, null=True)),
                ('date_b1', models.DateField(blank=True, null=True)),
                ('date_b2', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('a', '暫存中'), ('b', '申請中'), ('c', '已核准'), ('d', '已駁回')], max_length=1)),
                ('comment', models.CharField(blank=True, max_length=256)),
                ('staff_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.staff')),
            ],
        ),
    ]
