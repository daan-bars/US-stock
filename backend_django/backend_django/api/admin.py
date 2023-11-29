from django.contrib import admin

# Register your models here.
from .models import Stock, Historical, BackTesting, StrategySteps


class StrategyStepsInline(admin.TabularInline):
    model = StrategySteps
    extra = 0


@admin.register(BackTesting)
class BackTestingAdmin(admin.ModelAdmin):
    inlines = [StrategyStepsInline]


admin.site.register(Stock)
admin.site.register(Historical)
admin.site.register(StrategySteps)
