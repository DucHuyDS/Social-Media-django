from django.urls import path,include
from . import views


urlpatterns = [
    path('<int:user_id>/',views.chat,name='chat'),
    path('read_noti/',views.read_noti,name='read_noti'),
    path('mess_img/',views.mess_img,name='mess_img'),
]