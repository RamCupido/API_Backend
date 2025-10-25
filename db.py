import psycopg2

def get_connection():
    return psycopg2.connect(
        host="db",
        database="flask_login",
        user="admin",
        password="admin123",
    )