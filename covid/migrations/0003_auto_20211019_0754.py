# Generated by Django 3.1.5 on 2021-10-19 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0002_auto_20211019_0745'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={},
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_date1',
            field=models.DateField(blank=True, null=True, verbose_name='Последняя вакцинация (дата 1)'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_date2',
            field=models.DateField(blank=True, null=True, verbose_name='Последняя вакцинация (дата 2)'),
        ),
    ]
