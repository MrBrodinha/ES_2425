import pymysql

def lambda_handler(event, context):
    try:
        # Extract input data
        loan_id = event['loan_id']

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
            cursor.execute(f"UPDATE loans
                            SET 
                                amount_paid = amount_paid + monthly_payment, -- Increment the amount paid
                                status = CASE 
                                            WHEN (amount_paid + monthly_payment) >= (monthly_payment * duration) THEN 'PAID'
                                            ELSE status
                                        END
                            WHERE loan_id = {loan_id};")
            connection.commit()
    
        return {
            "statusCode": 200,
            "message": "Loan updated successfully"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }
    
    finally:
        connection.close()
