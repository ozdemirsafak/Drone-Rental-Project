from django.db import models
from app.models import BaseModel,Drone
from django.contrib.auth.models import User

class Order(BaseModel):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    renter_member = models.CharField(max_length=100)  
    rental_start_datetime = models.DateTimeField()
    rental_end_datetime = models.DateTimeField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

