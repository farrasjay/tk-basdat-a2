from django.shortcuts import render

# Create your views here.
def landing_page(request):
    return render(request, "landing_page.html")

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def register_panitia_page(request):
    return render(request, "register_panitia.html")

def register_manager_penonton_page(request):
    return render(request, "register_manager_penonton.html")

def dashboard_panitia_page(request):
    return render(request, "dashboard_panitia.html")

def dashboard_manager_penonton_page(request):
    return render(request, "dashboard_manager_penonton.html")