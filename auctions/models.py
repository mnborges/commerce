from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #watchlist = models.ManyToManyField(Listing, blank=True, related_name='watchlist') - need to declare Listing first
    def __str__(self):
        return f"@{self.username}: {self.email}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid =  models.DecimalField(max_digits= 8, decimal_places=2)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True, blank = True)
    status = models.BooleanField(default=True)
    image = models.URLField(null=True) 
    category = models.CharField(max_length=64, null=True, blank=True) #models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    def __str__(self):
        st = 'open' if self.status==True else  'closed'
        return f"{self.id}: listing of {self.title} created by {self.seller.username} is {st}"
        
class Bid(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(max_digits= 8, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    def __str__(self):
        return f"{self.id}: bid of {self.value} on {self.product.title} made by {self.bidder.username}"
 
class Comment(models.Model):
    date = models.DateTimeField(auto_now=True)
    content = models.TextField()
    page = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    def __str__(self):
        return f"{self.id}: comment made by {self.author.username} on {self.page.title} page"