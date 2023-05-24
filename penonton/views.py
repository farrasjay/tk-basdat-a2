import string
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
import random

forms = {}


@csrf_exempt
def get_list_stadium(request):
    result = query(f"SELECT * FROM stadium")
    context = {'stadiums': result}

    if request.method != "POST":
        return render(request, "pilih_stadium_tiket.html", context)
    else:
        context = {"isNotValid": False, "message": "Harap masukkan seluruh data"}

        stadium = request.POST["stadium"]
        tanggal = request.POST["date"]  # Update the name of the date field

        context["isNotValid"] = not stadium or not tanggal
        print(context["isNotValid"])

        if context["isNotValid"]:
            context["stadiums"] = result
            return render(request, "pilih_stadium_tiket.html", context)

        forms['stadium'] = stadium
        forms['tanggal'] = tanggal

        return redirect("/penonton/tiket/list-waktu")


@csrf_exempt
def get_list_time(request):
    result = query(f""" 
            SELECT concat(TO_CHAR(start_datetime,'HH:MI'), ' - ', TO_CHAR(end_datetime,'HH:MI')) as display, P.start_datetime::text FROM STADIUM S JOIN PERTANDINGAN P 
            ON S.id_stadium = P.stadium 
            WHERE P.stadium = '{forms['stadium']}'
            AND start_datetime::timestamp::date = '{forms['tanggal']}'
            """)
    print(result)

    nama_stadium = query(
        f"SELECT nama FROM STADIUM WHERE id_stadium = '{forms['stadium']}'")[0][0]
    context = {"list_waktu": result, "nama_stadium": nama_stadium}

    if request.method != "POST":
        return render(request, "pilih_waktu_tiket.html", context)
    else:
        waktu = request.POST['waktu']
        forms['waktu'] = waktu

    return redirect("/penonton/tiket/list-pertandingan")

@csrf_exempt
def get_list_pertandingan(request):
    result = query(f"""
            SELECT DISTINCT ON (P.id_pertandingan) P.id_pertandingan, A.nama_tim as tim_a, B.nama_tim as tim_b
            FROM PERTANDINGAN P, TIM_PERTANDINGAN A, TIM_PERTANDINGAN B, STADIUM S
            WHERE P.id_pertandingan = A.id_pertandingan
            AND P.id_pertandingan = B.id_pertandingan
            AND S.id_stadium = P.stadium
            AND A.nama_tim != B.nama_tim
            AND P.stadium = '{forms['stadium']}'
            AND P.start_datetime = '{forms['waktu']}'
            GROUP BY P.id_pertandingan, A.nama_tim, B.nama_tim;
            """)
    
    context = {"list_pertandingan": result}

    if request.method != "POST":
        return render(request, "pilih_pertandingan_tiket.html", context)
    else:
        pertandingan = request.POST['pertandingan']
        forms['pertandingan'] = pertandingan
    
        return redirect("/penonton/tiket/beli")

@csrf_exempt
def beli_tiket(request):
    jenis_list = ["VIP", "Main East", "kategori 1", "kategori 2"]
    pembayaran_list = ['Shopeepay', 'Gopay', 'OVO', 'Debit']
    context = {
        'jenis_list': jenis_list,
        'pembayaran_list': pembayaran_list,
        'isNotValid': False
    }

    if request.method != "POST":
        return render(request, "beli_tiket.html", context)
    else:
        jenis = request.POST['jenis']
        pembayaran = request.POST['pembayaran']

        lists = {}

        username = request.COOKIES['username']
        letters = string.ascii_uppercase
        lists['id_penonton'] = query(
            f"SELECT id_penonton FROM PENONTON WHERE username = '{username}'")[0][0]
        print(lists['id_penonton'])
        lists['pertandingan'] = forms["pertandingan"]
        lists['jenis'] = jenis
        lists['pembayaran'] = pembayaran
        lists['receipt'] = ''.join(random.choice(letters) for i in range(9))

        result = query(f"""INSERT INTO PEMBELIAN_TIKET VALUES 
            ('{lists['receipt']}', '{lists['id_penonton']}', '{lists['jenis']}', '{lists['pembayaran']}', '{lists['pertandingan']}') """)

        if isinstance(result, Exception):
            context['message'] = str(result).partition('CONTEXT')[0]
            context["isNotValid"] = True
            return render(request, "beli_tiket.html", context)

        return redirect("/authentication/dashboard_penonton")