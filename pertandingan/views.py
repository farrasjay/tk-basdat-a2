from django.shortcuts import render

from utils.query import query
from utils.users import get_user_role

# Create your views here.
def get_list_pertandingan(request):
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
    username = request.COOKIES['username']
    role = get_user_role(username)

    if (role == 'penonton'):
        return render(request, "list_pertandingan_penonton.html", context)
    else:
        return render(request, "list_pertandingan_manager.html", context)
