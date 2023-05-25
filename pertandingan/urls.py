from django.urls import path
from pertandingan.views import *

app_name = 'pertandingan'

urlpatterns = [
 path('list-pertandingan-penonton/', get_list_pertandingan_penonton, name='get_list_pertandingan_penonton'),
 path('list-pertandingan-manager/', get_list_pertandingan_manager, name='get_list_pertandingan_manager'),
]