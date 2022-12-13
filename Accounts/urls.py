
from django.urls import path
from . import views

urlpatterns = [
    path('',views.account,name='account'),
    path('search/',views.search,name='search'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('password/',views.password,name='password'),
]
