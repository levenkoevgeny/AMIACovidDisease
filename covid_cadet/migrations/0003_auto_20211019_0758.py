# Generated by Django 3.1.5 on 2021-10-19 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid_cadet', '0002_employeecadet_is_willing'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeecadet',
            name='last_date1',
            field=models.DateField(blank=True, null=True, verbose_name='Последняя вакцинация (дата 1)'),
        ),
        migrations.AddField(
            model_name='employeecadet',
            name='last_date2',
            field=models.DateField(blank=True, null=True, verbose_name='Последняя вакцинация (дата 2)'),
        ),
    ]
