from django.contrib import admin
from .models import *


admin.site.register(Subdivision)
admin.site.register(Employee)
admin.site.register(VaccineKind)
admin.site.register(VaccineCourse)
# admin.site.register(Vaccination)
admin.site.register(Position)
admin.site.register(Rank)

