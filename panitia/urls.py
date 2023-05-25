from django.urls import path
from panitia.views import *

app_name = 'panitia'

urlpatterns = [
  path('mulai-rapat/', mulai_rapat, name="mulai_rapat"),
  path('rapat/', isi_rapat, name="isi_rapat"),
  path('mulai-pertandingan/', mulai_pertandingan, name="mulai_pertandingan"),
  path('mulai-pertandingan/peristiwa', pilih_peristiwa, name="pilih_peristiwa"),
]
