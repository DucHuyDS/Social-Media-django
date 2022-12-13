from django.contrib import admin
from .models import Thread,Message,Notifications
# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display=['created_at']

class NotificationsAdmin(admin.ModelAdmin):
    list_display=['generator','user','timestamp']


admin.site.register(Thread)
admin.site.register(Message,MessageAdmin)
admin.site.register(Notifications,NotificationsAdmin)