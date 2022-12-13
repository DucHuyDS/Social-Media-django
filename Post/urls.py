from django.urls import path,include
from . import views


urlpatterns = [
    path('get_next_post/',views.get_next_post,name='get_next_post'),
    path('create_post/',views.create_post,name='create_post'),
    path('delete_post/<int:post_id>',views.delete_post,name='delete_post'),
    path('update_post/<int:post_id>',views.update_post,name='update_post'),
    path('share_post/<int:post_id>',views.share_post,name='share_post'),
    path('like/<int:post_id>',views.like,name='like'),
    path('like_comment/<int:comment_id>',views.like_comment,name='like_comment'),
    path('comment/<int:post_id>',views.comment,name='comment'),
    path('detail/<int:post_id>',views.detail,name='detail'),
    path('delete_comment/<int:comment_id>',views.delete_comment,name='delete_comment'),
    path('post_data/<int:post_id>',views.post_data,name='post_data'),
    path('post_data_share/<int:post_id>',views.post_data_share,name='post_data_share')
]