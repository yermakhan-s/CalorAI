from django.contrib import admin
from .models import MyUser, Calorie
# Register your models here.

class CalorieInline(admin.TabularInline):
    model = Calorie


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    inlines = [CalorieInline]

@admin.register(Calorie)
class CalorieAdmin(admin.ModelAdmin):
    pass
