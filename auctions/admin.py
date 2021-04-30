from django.contrib import admin
from .models import User, Listing

class UserAdmin(admin.ModelAdmin):
    list_display = ("username","first_name","last_name", "is_staff")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date","title","seller","status")
    
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)