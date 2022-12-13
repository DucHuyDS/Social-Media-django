from django.contrib import admin
from .models import Media,Post,CommentPost

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['author','created_at']



class MediaAdmin(admin.ModelAdmin):
    list_display=['post']

class CommentPostAdmin(admin.ModelAdmin):
    list_display=['post','created_at']

admin.site.register(Post,PostAdmin)
admin.site.register(Media,MediaAdmin)
admin.site.register(CommentPost,CommentPostAdmin)
