from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    photo = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Vaccine(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccines')
    name = models.CharField(max_length=100)
    date = models.DateField()
    next_due_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} para {self.pet.name} em {self.date}"
    
class Report(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report #{self.id} - {self.pet}"
    

