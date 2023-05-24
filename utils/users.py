from django.db import connection
from utils.db_utils import dict_fetch_all

def get_user_role(username):    
    with connection.cursor() as cursor:
        cursor.execute('SET SEARCH_PATH TO ULEAGUE;')
        
        # Check manajer
        cursor.execute(f'''
            SELECT *
            FROM manajer
            WHERE username='{username}';
        ''')
        user_list = dict_fetch_all(cursor)
        if len(user_list) != 0:
            return 'manajer'
    
        # Check penonton
        cursor.execute(f'''
            SELECT *
            FROM penonton
            WHERE username='{username}';
        ''')
        user_list = dict_fetch_all(cursor)
        if len(user_list) != 0:
            return 'penonton'
    
        # Check panitia
        cursor.execute(f'''
            SELECT *
            FROM panitia
            WHERE username='{username}';
        ''')
        user_list = dict_fetch_all(cursor)
        if len(user_list) != 0:
            return 'panitia'
    
    return 'none'

def check_user_availability(username, password):
    with connection.cursor() as cursor:
        cursor.execute('SET SEARCH_PATH TO ULEAGUE;')
        cursor.execute(f'''
            SELECT *
            FROM USER_SYSTEM
            WHERE username='{username}' AND password='{password}';
        ''')
        user_list = dict_fetch_all(cursor)
    if len(user_list) != 0: # User found
        return True
    else: # User not found
        return False