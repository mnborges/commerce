from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"@{self.username}: {self.email}"

class Group(models.Model):
    category = models.CharField(max_length=64, null=True, blank=True)
    def __str__(self):
        return f'{self.category}'

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid =  models.DecimalField(max_digits= 8, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True, editable=False)
    end_date = models.DateTimeField(null=True, blank = True)
    status = models.BooleanField(default=True)
    image = models.URLField(null=True, blank = True) 
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    on_watch = models.ManyToManyField(User, blank=True, related_name='watchlist')
    def __str__(self):
        st = 'open' if self.status==True else  'closed'
        return f"{self.id}: listing of {self.title} created by {self.seller.username} is {st}"
        
class Bid(models.Model):
    date = models.DateTimeField(auto_now_add=True, editable=False)
    value = models.DecimalField(max_digits= 8, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    def __str__(self):
        return f"{self.id}: bid of {self.value} on {self.product.title} made by {self.bidder.username}"
 
class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True, editable=False)
    content = models.TextField()
    page = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    def __str__(self):
        return f"{self.id}: comment made by {self.author.username} on {self.page.title} page"