from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('home/', landing_page, name='landing_page'),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('register_panitia/', register_panitia_page, name='register_panitia_page'),
    path('register_manager_penonton/', register_manager_penonton_page, name='register_manager_penonton_page'),
    path('dashboard_panitia/', dashboard_panitia_page, name='dashboard_panitia_page'),
    path('dashboard_manager_penonton/', dashboard_manager_penonton_page, name='dashboard_manager_penonton_page'),
]