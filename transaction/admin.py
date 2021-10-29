from django.contrib import admin
from .models import BuyModel
# Register your models here.

@admin.register(BuyModel)
class BuyModelAdmin(admin.ModelAdmin):
    list_display = ('id','video',)

