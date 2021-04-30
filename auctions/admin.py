from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("username","first_name","last_name", "is_staff")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date","title","seller","status")
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "date","product","bidder","value")   
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "date","page","author","content")  

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)