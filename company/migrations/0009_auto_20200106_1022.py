# Generated by Django 2.2.4 on 2020-01-06 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='boss0',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='boss1',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='boss2',
            field=models.IntegerField(blank=True),
        ),
    ]