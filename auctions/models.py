from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"@{self.username}: {self.email} ({self.first_name} {self.last_name}) "

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid =  models.DecimalField(max_digits= 8, decimal_places=2)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(blank=True)
    status = models.BooleanField(default=True)
    image = models.URLField(blank=True) 
    category = models.CharField(unique=True, blank=True, max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    def __str__(self):
        st = 'open' if self.status==True else  'closed'
        return f"listing of {self.title} created by {self.seller.username} is {st}"