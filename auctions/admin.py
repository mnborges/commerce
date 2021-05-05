from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("username","email", "is_staff")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date","title","seller","status")
    filter_horizontal = ("on_watch",)
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "date","product","bidder","value") 
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "date","page","author","content") 
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "category")  
    
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Group,GroupAdmin)