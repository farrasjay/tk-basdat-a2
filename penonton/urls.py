from django.urls import path
from penonton.views import *

app_name = 'penonton'

urlpatterns = [
  path('tiket/list-stadium', get_list_stadium, name="get_list_stadium"),
  path('tiket/list-waktu', get_list_time, name="get_list_time"),
  path('tiket/list-pertandingan', get_list_pertandingan, name="get_list_pertandingan"),
  path('tiket/beli', beli_tiket, name="beli_tiket"),
  # path('pertandingan/', list_pertandingan, name="list_pertandingan"),
]
