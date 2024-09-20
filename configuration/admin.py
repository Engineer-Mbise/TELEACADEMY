from django.contrib import admin

# Register your models here.


from .models import Payment
from .models import Progress
from .models import Level
from .models import Gender
from courses.models import Registered


class LevelAdmin(admin.ModelAdmin):
    list_display = ["name"]


class GenderAdmin(admin.ModelAdmin):
    list_display = ["acronym", "description"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["payment_status"]


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ["progress_status"]

admin.site.register(Level, LevelAdmin)
admin.site.register(Gender, GenderAdmin)
