# Create your models here.
from django.db import models
import pymysql

connection = pymysql.connect(
    host='database-1.cd0keqmiesi5.us-east-1.rds.amazonaws.com',
    user='admin',
    password='GvUFyayd)42Q8tgnguknBNCJ<QTQ',
    database='users-info',
    port=3306
)

def get_all_clients():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM clients")
        return cursor.fetchall()

def get_client_by_username(username):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM clients WHERE username = '{username}'")
        return cursor.fetchone()

def get_client_by_email(email):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM clients WHERE email = '{email}'")
        return cursor.fetchone()
    

def get_last_loan_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(loan_id) FROM Loans")
        return cursor.fetchone()[0]
    
    
