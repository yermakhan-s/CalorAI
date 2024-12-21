from django.db import models
from django.utils import timezone
# Create your models here.
class MyUser(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    tokens = models.IntegerField(default=20)
    created_date = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=10, default='en', null=True, blank=True) 

    def __str__(self):
        return self.username if self.username else self.id

class Calorie(models.Model):
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='calories')
    description = models.TextField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)
    proteins = models.IntegerField(blank=True, null=True)
    fats = models.IntegerField(blank=True, null=True)
    carbohydrates = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user}  {self.created_date}"

