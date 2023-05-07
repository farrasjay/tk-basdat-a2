from django.shortcuts import render

# Create your views here.
def pilih_stadium(request):
  return render(request, "pilih_stadium.html")

def waktu_stadium(request):
  return render(request, "list_waktu_stadium.html")

def list_pertandingan_tiket(request):
  return render(request, "list_pertandingan_tiket.html")

def beli_tiket(request):
  return render(request, "beli_tiket.html")

def list_pertandingan(request):
  return render(request, "pertandingan.html")