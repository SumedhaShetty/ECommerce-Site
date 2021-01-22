from django.contrib import admin
from django.urls import path,include
from . import views
app_name = "main_app"

urlpatterns = [

    path('main_app/',include("main_app.urls")),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
]