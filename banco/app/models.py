# Create your models here.
from django.db import models
import pymysql

connection = pymysql.connect(
    host='bruh, ver no aws rds',
    user='admin',
    password='bruh, ver no aws console manager ou secret manager whatever',
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
    
    
