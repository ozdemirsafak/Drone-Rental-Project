from django.db import models
from app.models import BaseModel

class Drone(models.Model):  
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'drones'

    def __str__(self):
        return self.name
