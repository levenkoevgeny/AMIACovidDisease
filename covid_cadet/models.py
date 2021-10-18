from django.db import models
from django.contrib.auth.models import User
from covid.models import Rank, Position


class SubdivisionCadet(models.Model):
    subdivision_name = models.CharField(verbose_name="Подразделение", max_length=255)
    subdivision_short_name = models.CharField(
        verbose_name="Короткое название подразделения (только заглавные английские буквы)", max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Кто может вносить изменения", blank=True,
                              null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего редактирования", blank=True, null=True)

    def __str__(self):
        return str(self.subdivision_name)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Факультет'
        verbose_name_plural = '1. Факультеты'


class Course(models.Model):
    course_name = models.CharField(verbose_name="Курс", max_length=255)
    faculty = models.ForeignKey(SubdivisionCadet, verbose_name="Факультет", on_delete=models.SET_NULL, blank=True,
                                null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего редактирования", auto_now=True,
                                         blank=True, null=True)

    def __str__(self):
        return self.course_name + ' ' + self.faculty.subdivision_name

    class Meta:
        ordering = ('course_name',)
        verbose_name = 'Курс'
        verbose_name_plural = '2. Курсы'


class Group(models.Model):
    group_name = models.CharField(verbose_name="Группа", max_length=255)
    course = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.SET_NULL, blank=True,
                               null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего редактирования", auto_now=True,
                                         blank=True, null=True)

    def __str__(self):
        return str(self.group_name) + ' ' + str(self.course.course_name) + ' ' + str(self.course.faculty)

    class Meta:
        ordering = ('group_name',)
        verbose_name = 'Группа'
        verbose_name_plural = '3. Группы'


class EmployeeCadet(models.Model):
    SEX = [
        (1, 'Мужской'),
        (2, 'Женский'),
    ]

    WORK_STATUS = [
        (1, 'Работает'),
        (2, 'Уволен'),
    ]

    MARITAL_STATUS = [
        (1, 'Холостой/Не замужем'),
        (2, 'Женат/Замужем'),
        (3, 'Разведен/Разведена'),
        (4, 'Вдова/Вдовец'),
    ]

    last_name = models.CharField(verbose_name="Фамилия", max_length=30)
    first_name = models.CharField(verbose_name="Имя", max_length=30, blank=True, null=True)
    patronymic = models.CharField(verbose_name="Отчество", max_length=30, blank=True, null=True)
    group_fk = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.SET_NULL, blank=True,
                                 null=True)
    sex = models.IntegerField(choices=SEX, verbose_name="Пол", blank=True, null=True)
    work_status = models.IntegerField(choices=WORK_STATUS, verbose_name="Рабочий статус", default=1)
    marital_status = models.IntegerField(choices=MARITAL_STATUS, verbose_name="Семейное положение", blank=True,
                                         null=True)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, verbose_name="Звание", blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, verbose_name="Должность", blank=True, null=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=30, blank=True, null=True)
    address = models.CharField(verbose_name="Адрес", max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    date_of_death = models.DateField(verbose_name="Дата смерти", blank=True, null=True)
    has_contraindications = models.BooleanField(verbose_name="Имеет противопоказания к прививке", default=False)
    contraindications_explain = models.TextField(verbose_name="Пояснение к противопоказаниям", blank=True, null=True)
    is_willing = models.BooleanField(verbose_name="Желает пройти вакцинацию", default=False)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего редактирования", auto_now=True)

    def __str__(self):
        return self.last_name

    class Meta:
        ordering = ('last_name',)
        verbose_name = 'Курсант'
        verbose_name_plural = '4. Курсанты'
