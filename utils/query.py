from django.db import connection, DatabaseError, IntegrityError
from collections import namedtuple


def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def query(query_str: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO 'uleague'")
            cursor.execute(query_str)

            if query_str.strip().lower().startswith("select"):
                # Return the result as a list of namedtuples
                desc = cursor.description
                nt_result = namedtuple("Result", [col[0] for col in desc])
                return [nt_result(*row) for row in cursor.fetchall()]
            else:
                # Return the rowcount for non-select queries
                return cursor.rowcount

    except (DatabaseError, IntegrityError) as e:
        # Handle database errors
        return str(e)
    except Exception as e:
        # Handle other exceptions
        return f"An error occurred: {str(e)}"

