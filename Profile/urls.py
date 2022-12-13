from django.urls import path,include
from . import views


urlpatterns = [
    path('<str:username>/posts',views.posts,name='posts'),
    path('<str:username>/about',views.about,name='about'),
    path('<str:username>/friends',views.friends,name='friends'),
    path('<str:username>/media',views.media,name='media'),
    path('send_friend_request/<int:user_id>',views.send_friend_request,name='send_friend_request'),
    path('accept_friend_request/<int:user_id>',views.accept_friend_request,name='accept_friend_request'),
    path('remove_friend/<int:user_id>',views.remove_friend,name='remove_friend'),
    path('contact/',views.contact,name='contact'),
]