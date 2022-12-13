from django.contrib import admin
from .models import  Account
from Profile.models import Profile

# Register your models here.
class ProfileInline(admin.TabularInline):
    model=Profile
    extra=1

class AccoutAdmin(admin.ModelAdmin):
    list_display=['email','username','first_name','last_name','phone','date_joined','last_login','is_active','is_staff','is_admin']
    readonly_fields=['date_joined','last_login']
    search_fields=['email']
    inlines=[ProfileInline]

admin.site.register(Account,AccoutAdmin)