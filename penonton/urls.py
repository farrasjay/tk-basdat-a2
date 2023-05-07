from django.urls import path
from penonton.views import *

app_name = 'penonton'

urlpatterns = [
  path('tiket/', pilih_stadium, name="pilih_stadium"),
  path('tiket/waktu', waktu_stadium, name="waktu_stadium"),
  path('tiket/waktu/pertandingan', list_pertandingan_tiket, name="list_pertandingan_tiket"),
  path('tiket/waktu/pertandingan/beli', beli_tiket, name="beli_tiket"),
  path('pertandingan/', list_pertandingan, name="list_pertandingan"),
]
