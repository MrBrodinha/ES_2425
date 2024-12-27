import pymysql

def lambda_handler(event, context):
    try:
        # Extract input data
        user_id = event.get("user_id", "")
        yearly_income = float(event.get("yearly_income", 0))
        amount = float(event.get("amount", 0))
        duration = int(event.get("duration", 0))
        monthly_payment = float(event.get("monthly_payment", 0))
        answer = event.get("answer", "")
    except Exception as e:
        return {
            "statusCode": 400,
            "error": str(e)
        }

    try:
        connection = pymysql.connect(
            host='database-1.cd0keqmiesi5.us-east-1.rds.amazonaws.com',
            user='admin',
            password='GvUFyayd)42Q8tgnguknBNCJ<QTQ',
            database='users-info',
            port=3306
        )

        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO loans (user_id, yearly_income, amount, duration, monthly_payment, answer) VALUES ('{user_id}', {yearly_income}, {amount}, {duration}, {monthly_payment}, '{answer}')")
            connection.commit()
    
        return {
            "statusCode": 200,
            "message": "Loan request successfully submitted"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }
    
    finally:
        connection.close()
