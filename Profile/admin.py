from django.contrib import admin
from .models import  Profile,FriendRequest
# Register your models here.

class FriendRequestAdmin(admin.ModelAdmin):
    list_display=['sender','receiver']

admin.site.register(Profile)
admin.site.register(FriendRequest,FriendRequestAdmin)