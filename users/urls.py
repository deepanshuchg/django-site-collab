from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('',views.index, name='index'),
   path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
   path('logout', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
   path('register', views.register, name='register'),
   path('youtube', views.youtube, name='youtube')
]