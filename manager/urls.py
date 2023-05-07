from django.urls import path
from manager.views import *

app_name = 'manager'

urlpatterns = [
  path('history-rapat/', history_rapat, name="history_rapat"),
]
