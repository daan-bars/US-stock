from django.contrib import admin

# Register your models here.
from .models import Stock, Historical

admin.site.register(Stock)
admin.site.register(Historical)
