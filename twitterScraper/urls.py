from django.contrib import admin
from django.urls import path,include
from . import views




urlpatterns = [
    path('', views.home_page, name='home'),
    path('search/<str:keyword>', views.insert, name='insert'),
    path('login', views.login_page, name='login'),
    path('register', views.registration_page, name='register'),
    path('register_user', views.register_user, name='register_user'),
    path('login_user', views.user_login, name='login_user'),
    path('analytics/<str:keyword>', views.analytics, name='analytics'),
    path('analyze/<str:keyword>', views.get_keyword, name='get_keyword'),
    path('error', views.return_error_page, name='get_error'),
    

]

    