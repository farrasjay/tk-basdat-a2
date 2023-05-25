from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from utils.db_utils import dict_fetch_all
from utils.users import get_user_role
import uuid

# Create your views here.
def landing_page(request):
    return render(request, "landing_page.html")

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def dashboard_panitia_page(request):
    return render(request, "dashboard_panitia.html")

def dashboard_manajer_page(request):
    return render(request, "dashboard_manajer.html")

def dashboard_penonton_page(request):
    return render(request, "dashboard_penonton.html")

def register_panitia_page(request):
    if request.method == 'POST':
        newPanitiaUUID = uuid.uuid4()
        username = request.POST.get("usernameField")
        password = request.POST.get("passwordField")
        nama_depan = request.POST.get("firstNameField")
        nama_belakang = request.POST.get("lastNameField")
        nomor_hp = request.POST.get("phoneNumberField")
        email = request.POST.get("emailField")
        alamat = request.POST.get("addressField")
        status = request.POST.get("statusField")
        jabatan = request.POST.get("jabatanField")

        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO ULEAGUE;")
            cursor.execute(f"""
                INSERT INTO USER_SYSTEM VALUES ('{username}','{password}');
                INSERT INTO NON_PEMAIN (id_non_pemain, nama_depan, nama_belakang, nomor_hp, email, alamat) VALUES ('{newPanitiaUUID}', '{nama_depan}', '{nama_belakang}', '{nomor_hp}', '{email}', '{alamat}');
                INSERT INTO STATUS_NON_PEMAIN (id_non_pemain, status) VALUES ('{newPanitiaUUID}', '{status}');
                INSERT INTO PANITIA (id_panitia, jabatan, username) VALUES ('{newPanitiaUUID}', '{jabatan}', '{username}');
            """)

            response = HttpResponse()
            response.status_code = 200

        return redirect('authentication:login_page')
    return render(request, "register_panitia.html")

def register_manager_page(request):
    if request.method == 'POST':
        print("MASUK REG MANAJER")
        newManajerUUID = uuid.uuid4()
        username = request.POST.get("usernameField")
        password = request.POST.get("passwordField")
        nama_depan = request.POST.get("firstNameField")
        nama_belakang = request.POST.get("lastNameField")
        nomor_hp = request.POST.get("phoneNumberField")
        email = request.POST.get("emailField")
        alamat = request.POST.get("addressField")
        status = request.POST.get("statusField")

        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO ULEAGUE;")
            cursor.execute(f"""
                INSERT INTO USER_SYSTEM VALUES ('{username}','{password}');
                INSERT INTO NON_PEMAIN (id_non_pemain, nama_depan, nama_belakang, nomor_hp, email, alamat) VALUES ('{newManajerUUID}', '{nama_depan}', '{nama_belakang}', '{nomor_hp}', '{email}', '{alamat}');
                INSERT INTO STATUS_NON_PEMAIN (id_non_pemain, status) VALUES ('{newManajerUUID}', '{status}');
                INSERT INTO MANAJER (id_manajer, username) VALUES ('{newManajerUUID}', '{username}');
            """)

            response = HttpResponse()
            response.status_code = 200

        return redirect('authentication:login_page')
    return render(request, "register_manager.html")

def register_penonton_page(request):
    if request.method == 'POST':
        newPenontonUUID = uuid.uuid4()
        username = request.POST.get("usernameField")
        password = request.POST.get("passwordField")
        nama_depan = request.POST.get("firstNameField")
        nama_belakang = request.POST.get("lastNameField")
        nomor_hp = request.POST.get("phoneNumberField")
        email = request.POST.get("emailField")
        alamat = request.POST.get("addressField")
        status = request.POST.get("statusField")

        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO ULEAGUE;")
            cursor.execute(f"""
                INSERT INTO USER_SYSTEM VALUES ('{username}','{password}');
                INSERT INTO NON_PEMAIN (id_non_pemain, nama_depan, nama_belakang, nomor_hp, email, alamat) VALUES ('{newPenontonUUID}', '{nama_depan}', '{nama_belakang}', '{nomor_hp}', '{email}', '{alamat}');
                INSERT INTO STATUS_NON_PEMAIN (id_non_pemain, status) VALUES ('{newPenontonUUID}', '{status}');
                INSERT INTO PENONTON (id_penonton, username) VALUES ('{newPenontonUUID}', '{username}');
            """)

            response = HttpResponse()
            response.status_code = 200

        return redirect('authentication:login_page')
    return render(request, "register_penonton.html")

def login_user_system(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    elif request.method == 'POST':
        response = HttpResponse()
        username = request.POST['username']
        password = request.POST['password']
        with connection.cursor() as cursor:
            cursor.execute('SET SEARCH_PATH TO ULEAGUE;')
            cursor.execute(f'''
                SELECT *
                FROM USER_SYSTEM
                WHERE username='{username}' AND password='{password}';
            ''')
            user_list = dict_fetch_all(cursor)
        if len(user_list) != 0:  # User found
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            response.status_code = 200
            return response
        else:  # User not found
            response.delete_cookie('username')
            response.delete_cookie('password')
            response.status_code = 404
            return response
    return HttpResponse(status=404)
            
def logout_user_system(request):
    response = HttpResponse(status=200)
    response.delete_cookie('username')
    response.delete_cookie('password')
    return redirect('authentication:landing_page')

def dashboard(request):
    username = request.COOKIES['username']
    role = get_user_role(username)

    context = {
        'user': {
            'role': f'{role}',
        }
    }

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO ULEAGUE;")

        if role == 'manajer':
            cursor.execute(f"""
                SELECT * 
                FROM USER_SYSTEM
                WHERE username='{username}';
            """)

            data = dict_fetch_all(cursor)
            context['data'] = data[0]

            cursor.execute(f"""
                SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, SNP.status
                FROM USER_SYSTEM AS US
                JOIN MANAJER AS MJ ON US.username = MJ.username
                JOIN NON_PEMAIN AS NP ON MJ.id_manajer = NP.id_non_pemain
                JOIN STATUS_NON_PEMAIN AS SNP ON NP.id_non_pemain = SNP.id_non_pemain
                WHERE US.username = '{username}';
            """)

            manajer_dashboard_data = dict_fetch_all(cursor)
            context['manajer_dashboard_data'] = manajer_dashboard_data[0]

            cursor.execute(f"""
                SELECT TIM.nama_tim, TIM.universitas
                FROM USER_SYSTEM AS US
                JOIN MANAJER AS MJ ON US.username = MJ.username
                JOIN TIM_MANAJER AS TM ON MJ.id_manajer = TM.id_manajer
                JOIN TIM ON TM.nama_tim = TIM.nama_tim
                WHERE US.username = '{username}';
            """)

            manajer_tim_data = dict_fetch_all(cursor)

            if not manajer_tim_data:
                context['manajer_tim_data'] = None
                return render(request, 'dashboard_manajer.html', context)

            context['manajer_tim_data'] = manajer_tim_data[0]

            return render(request, 'dashboard_manajer.html', context)

        elif role == 'penonton':
            cursor.execute(f"""
                SELECT * 
                FROM USER_SYSTEM
                WHERE username='{username}';
            """)

            data = dict_fetch_all(cursor)
            context['data'] = data[0]

            cursor.execute(f"""
                SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, SNP.status
                FROM USER_SYSTEM AS US
                JOIN PENONTON AS PNT ON US.username = PNT.username
                JOIN NON_PEMAIN AS NP ON PNT.id_penonton = NP.id_non_pemain
                JOIN STATUS_NON_PEMAIN AS SNP ON NP.id_non_pemain = SNP.id_non_pemain
                WHERE US.username = '{username}';
            """)

            penonton_dashboard_data = dict_fetch_all(cursor)
            context['penonton_dashboard_data'] = penonton_dashboard_data[0]

            cursor.execute(f"""
                SELECT PTKT.jenis_tiket, STM.nama, STM.alamat, TGN.start_datetime, TGN.end_datetime
                FROM USER_SYSTEM AS US
                JOIN PENONTON AS PNT ON US.username = PNT.username
                JOIN PEMBELIAN_TIKET AS PTKT ON PNT.id_penonton = PTKT.id_penonton
                JOIN PERTANDINGAN AS TGN ON PTKT.id_pertandingan = TGN.id_pertandingan
                JOIN STADIUM AS STM ON TGN.stadium = STM.id_stadium
                WHERE US.username = '{username}';
            """)

            penonton_pertandingan_data = dict_fetch_all(cursor)

            if not penonton_pertandingan_data:
                context['penonton_pertandingan_data'] = None
                return render(request, 'dashboard_penonton.html', context)
            
            context['penonton_pertandingan_data'] = penonton_pertandingan_data[0]

            return render(request, 'dashboard_penonton.html', context)

        elif role == 'panitia':
            cursor.execute(f"""
                SELECT * 
                FROM USER_SYSTEM
                WHERE username='{username}';
            """)

            data = dict_fetch_all(cursor)
            context['data'] = data[0]

            cursor.execute(f"""
                SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, SNP.status, jabatan
                FROM USER_SYSTEM AS US
                JOIN PANITIA AS PTA ON US.username = PTA.username
                JOIN NON_PEMAIN AS NP ON PTA.id_panitia = NP.id_non_pemain
                JOIN STATUS_NON_PEMAIN AS SNP ON NP.id_non_pemain = SNP.id_non_pemain
                WHERE US.username = '{username}';
            """)

            panitia_dashboard_data = dict_fetch_all(cursor)
            context['panitia_dashboard_data'] = panitia_dashboard_data[0]

            cursor.execute(f"""
                SELECT id_pertandingan, datetime, isi_rapat
                FROM USER_SYSTEM AS US
                JOIN PANITIA AS PTA ON US.username = PTA.username
                JOIN RAPAT AS RPT ON PTA.id_panitia = RPT.perwakilan_panitia
                WHERE US.username = '{username}';
            """)

            panitia_rapat_data = dict_fetch_all(cursor)

            if not panitia_rapat_data:
                context['panitia_rapat_data'] = None
                return render(request, 'dashboard_panitia.html', context)

            context['panitia_rapat_data'] = panitia_rapat_data[0]

            return render(request, 'dashboard_panitia.html', context)
    