# Generated by Django 3.1.5 on 2021-10-18 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
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
                ('is_willing', models.BooleanField(default=False, verbose_name='Желает пройти вакцинацию')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Дата и время последнего редактирования')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'ordering': ('last_name',),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(max_length=50, verbose_name='Фамилия')),
            ],
            options={
                'verbose_name': 'Звание',
                'verbose_name_plural': 'Звания',
                'ordering': ('rank',),
            },
        ),
        migrations.CreateModel(
            name='VaccineKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=30, verbose_name='Вид вакцины')),
                ('is_one_component', models.BooleanField(default=False, verbose_name='Является однокомпонентной')),
            ],
            options={
                'verbose_name': 'Вид вакцины',
                'verbose_name_plural': 'Виды вакцины',
                'ordering': ('kind',),
            },
        ),
        migrations.CreateModel(
            name='VaccineCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date1', models.DateField(blank=True, null=True, verbose_name='Дата проведения первой вакцинации')),
                ('date2', models.DateField(blank=True, null=True, verbose_name='Дата проведения второй вакцинации')),
                ('add_date_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Дата и время последнего редактирования')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.employee', verbose_name='Сотрудник/курсант')),
                ('vaccine_kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.vaccinekind', verbose_name='Вид вакцины')),
            ],
            options={
                'verbose_name': 'Курс вакцинации',
                'verbose_name_plural': 'Курсы вакцинации',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Subdivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subdivision_name', models.CharField(max_length=255, verbose_name='Подразделение')),
                ('subdivision_short_name', models.CharField(max_length=255, verbose_name='Короткое название подразделения (только заглавные английские буквы)')),
                ('last_modified', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время последнего редактирования')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Кто может вносить изменения')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
                'ordering': ('subdivision_name',),
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='covid.position', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='employee',
            name='rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='covid.rank', verbose_name='Звание'),
        ),
        migrations.AddField(
            model_name='employee',
            name='subdivision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='covid.subdivision', verbose_name='Подразделение'),
        ),
    ]