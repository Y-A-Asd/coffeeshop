from django.contrib import admin

# Register your models here.
from .models import Offkey


@admin.register(Offkey)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active','mode']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
