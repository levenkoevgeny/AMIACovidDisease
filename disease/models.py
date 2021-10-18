from django.db import models
from covid.models import Employee


class DiseaseName(models.Model):
    disease_name = models.CharField(max_length=255, verbose_name="Болезнь")

    def __str__(self):
        return self.disease_name

    class Meta:
        ordering = ('disease_name',)
        verbose_name = 'Болезнь'
        verbose_name_plural = 'Болезни'


class HealthStatus(models.Model):
    health_status = models.CharField(max_length=255, verbose_name="Состояние здоровья")

    def __str__(self):
        return self.health_status

    class Meta:
        ordering = ('health_status',)
        verbose_name = 'Состояние здоровья'
        verbose_name_plural = 'Состояния здоровья'


class Consequence(models.Model):
    consequence = models.CharField(max_length=255, verbose_name="Последствие")

    def __str__(self):
        return self.consequence

    class Meta:
        ordering = ('consequence',)
        verbose_name = 'Последствие болезни'
        verbose_name_plural = 'Последствия болезни'


class Disease(models.Model):
    DISEASE_KIND = [
        (1, 'Карантин'),
        (2, 'Болезнь'),
    ]

    WHERE_TREATED = [
        (1, 'Дома'),
        (2, 'В учреждении здравоохранения'),
    ]
    disease_kind = models.IntegerField(choices=DISEASE_KIND, verbose_name="Тип записи")
    disease = models.ForeignKey(DiseaseName, on_delete=models.CASCADE, verbose_name="Болезнь", blank=True, null=True)
    employee = models.ForeignKey(Employee, verbose_name="Сотрудник", on_delete=models.CASCADE)
    date_of_application = models.DateField(verbose_name="Дата обращения к врачу", blank=True, null=True)
    date_of_analysis = models.DateField(verbose_name="Дата сдачи анализа", blank=True, null=True)
    date_of_confirmation = models.DateField(verbose_name="Дата получения результата анализа", blank=True, null=True)
    date_of_begin = models.DateField(verbose_name="Дата начала больничного/карантина", blank=True, null=True)
    date_of_end = models.DateField(verbose_name="Дата окончания больничного/карантина", blank=True, null=True)
    diagnosis = models.TextField(verbose_name="Диагноз", blank=True, null=True)
    where_treated = models.IntegerField(choices=WHERE_TREATED, verbose_name="Где лечится")
    health_status = models.ForeignKey(HealthStatus, on_delete=models.SET_NULL, verbose_name="Состояние здоровья", blank=True, null=True)
    consequence = models.ForeignKey(Consequence, on_delete=models.SET_NULL, verbose_name="Последствие болезни", blank=True, null=True)
    extra_data = models.TextField(verbose_name="Дополнительная информация", blank=True, null=True)

    def __str__(self):
        return self.employee.last_name

    @property
    def get_disease_kind(self):
        return self.DISEASE_KIND[self.disease_kind-1][1]

    @property
    def get_where_treated(self):
        return self.WHERE_TREATED[self.where_treated - 1][1]

    class Meta:
        ordering = ('employee',)
        verbose_name = 'Больничный/карантин'
        verbose_name_plural = 'Больничные/карантины'