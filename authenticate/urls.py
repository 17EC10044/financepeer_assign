from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),

]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
