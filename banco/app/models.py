# Create your models here.
import pymysql

connection = pymysql.connect(
    host='database-1.cd0keqmiesi5.us-east-1.rds.amazonaws.com',
    user='admin',
    password='GvUFyayd)42Q8tgnguknBNCJ<QTQ',
    database='users-info',
    port=3306
)

def get_all_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

def get_user_by_username(username):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
        return cursor.fetchone()

def get_user_by_email(email):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
        return cursor.fetchone()
    

def get_last_loan_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(loan_id) FROM loans")
        return cursor.fetchone()[0]
    
def get_loans_by_officer_id(loan_officer_id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM loans WHERE loan_officer_id = {loan_officer_id}")
        return cursor.fetchall()
    
def get_loan_by_id(loan_id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM loans WHERE loan_id = {loan_id}")
        return cursor.fetchone()

def get_loans_by_user_id(user_id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM loans WHERE user_id = '{user_id}'")
        return cursor.fetchall()
    
def get_slot_interviews_by_loan_id(loan_id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM interview_slot WHERE loan_id = '{loan_id}'")
        return cursor.fetchall()
    
def update_loan_status_by_loan_id(loan_id, status):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE loans SET answer = '{status}' WHERE loan_id = {loan_id}")
        connection.commit()