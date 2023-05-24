from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('home/', landing_page, name='landing_page'),
    path('login/', login_page, name='login_page'),
    path('login-user/', login_user_system, name='login_user_system'),
    path('logout-user/', logout_user_system, name='logout_user_system'),
    path('register/', register_page, name='register_page'),
    path('register_panitia/', register_panitia_page, name='register_panitia_page'),
    path('register_manager/', register_manager_page, name='register_manager_page'),
    path('register_penonton/', register_penonton_page, name='register_penonton_page'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('dashboard_panitia/', dashboard_panitia_page, name='dashboard_panitia_page'),
    path('dashboard_manajer/', dashboard_manajer_page, name='dashboard_manajer_page'),
    path('dashboard_penonton/', dashboard_penonton_page, name='dashboard_penonton_page'),
]