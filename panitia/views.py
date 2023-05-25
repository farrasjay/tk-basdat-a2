from django.shortcuts import render

# Create your views here.
def mulai_rapat(request):
  return render(request, "mulai_rapat.html")

def isi_rapat(request):
  return render(request, "isi_rapat.html")

def mulai_pertandingan(request):
  return render(request, "mulai_pertandingan.html")

def pilih_peristiwa(request):
  return render(request, "pilih_peristiwa.html")

