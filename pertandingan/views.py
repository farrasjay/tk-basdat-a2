from django.shortcuts import render

from utils.query import query

# Create your views here.
def get_list_pertandingan_penonton(request):
    result = query(f"""
            SELECT DISTINCT ON (P.id_pertandingan) P.id_pertandingan, A.nama_tim as tim_a, B.nama_tim as tim_b, S.nama as stadium, concat(TO_CHAR(P.start_datetime::timestamp::date, ' DD Month YYYY'), ', ', TO_CHAR(start_datetime,'HH:MI'), ' - ', TO_CHAR(end_datetime,'HH:MI')) as display  
            FROM PERTANDINGAN P, TIM_PERTANDINGAN A, TIM_PERTANDINGAN B, STADIUM S
            WHERE P.id_pertandingan = A.id_pertandingan
            AND P.id_pertandingan = B.id_pertandingan
            AND S.id_stadium = P.stadium
            AND A.nama_tim != B.nama_tim
            GROUP BY P.id_pertandingan, A.nama_tim, B.nama_tim, S.nama;
            """)
    
    context = {"list_pertandingan": result}

    return render(request, "list_pertandingan_penonton.html", context)
    
def get_list_pertandingan_manager(request):
    username = request.COOKIES["username"]
    id_manajer = query(
        f"SELECT id_manajer FROM MANAJER WHERE username = '{username}'")[0][0]
    result = query(f"""
            SELECT P.id_pertandingan, A.nama_tim as tim_a, B.nama_tim as tim_b, S.nama as stadium, concat(TO_CHAR(P.start_datetime::timestamp::date, ' DD Month YYYY'), ', ', TO_CHAR(start_datetime,'HH:MI'), ' - ', TO_CHAR(end_datetime,'HH:MI')) as display  
            FROM PERTANDINGAN P, TIM_PERTANDINGAN A, TIM_PERTANDINGAN B, STADIUM S, TIM_MANAJER TM
            WHERE P.id_pertandingan = A.id_pertandingan
            AND P.id_pertandingan = B.id_pertandingan
            AND S.id_stadium = P.stadium
            AND A.nama_tim != B.nama_tim
            AND TM.id_manajer = '{id_manajer}'
            AND TM.nama_tim = A.nama_tim
            GROUP BY P.id_pertandingan, A.nama_tim, B.nama_tim, S.nama;
            """)
    
    context = {"list_pertandingan": result}

    return render(request, "list_pertandingan_manager.html", context)
