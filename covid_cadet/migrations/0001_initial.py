# Generated by Django 3.1.5 on 2021-10-18 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('covid', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255, verbose_name='Курс')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата и время последнего редактирования')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': '2. Курсы',
                'ordering': ('course_name',),
            },
        ),
        migrations.CreateModel(
            name='SubdivisionCadet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subdivision_name', models.CharField(max_length=255, verbose_name='Подразделение')),
                ('subdivision_short_name', models.CharField(max_length=255, verbose_name='Короткое название подразделения (только заглавные английские буквы)')),
                ('last_modified', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время последнего редактирования')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Кто может вносить изменения')),
            ],
            options={
                'verbose_name': 'Факультет',
                'verbose_name_plural': '1. Факультеты',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255, verbose_name='Группа')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата и время последнего редактирования')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='covid_cadet.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': '3. Группы',
                'ordering': ('group_name',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeCadet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, max_length=30, null=True, verbose_name='Отчество')),
                ('sex', models.IntegerField(blank=True, choices=[(1, 'Мужской'), (2, 'Женский')], null=True, verbose_name='Пол')),
                ('work_status', models.IntegerField(choices=[(1, 'Работает'), (2, 'Уволен')], default=1, verbose_name='Рабочий статус')),
                ('marital_status', models.IntegerField(blank=True, choices=[(1, 'Холостой/Не замужем'), (2, 'Женат/Замужем'), (3, 'Разведен/Разведена'), (4, 'Вдова/Вдовец')], null=True, verbose_name='Семейное положение')),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Дата смерти')),
                ('has_contraindications', models.BooleanField(default=False, verbose_name='Имеет противопоказания к прививке')),
                ('contraindications_explain', models.TextField(blank=True, null=True, verbose_name='Пояснение к противопоказаниям')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Дата и время последнего редактирования')),
                ('group_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='covid_cadet.group', verbose_name='Группа')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='covid.position', verbose_name='Должность')),
                ('rank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='covid.rank', verbose_name='Звание')),
            ],
            options={
                'verbose_name': 'Курсант',
                'verbose_name_plural': '4. Курсанты',
                'ordering': ('last_name',),
            },
        ),
        migrations.AddField(
            model_name='course',
            name='faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='covid_cadet.subdivisioncadet', verbose_name='Факультет'),
        ),
    ]
