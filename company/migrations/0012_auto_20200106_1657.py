# Generated by Django 2.2.4 on 2020-01-06 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='b0',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='b1',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='b2',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
