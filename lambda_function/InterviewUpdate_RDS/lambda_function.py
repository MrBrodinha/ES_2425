import pymysql

def lambda_handler(event, context):
    try:
        # Extract input data
        loan_id = event['loan_id']
        interview_id = event['interview_id']

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
            cursor.execute(f"""UPDATE interview_slot
                                SET is_slot_chosen = TRUE
                                WHERE loan_id = {loan_id} AND id = {interview_id}
                                """)
            connection.commit()

        with connection.cursor() as cursor:
            cursor.execute(f"""DELETE FROM interview_slot
                                WHERE loan_id = {loan_id} AND is_slot_chosen = FALSE
                                """)
            connection.commit()
    
        return {
            "statusCode": 200,
            "message": "Interview updated successfully"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }
    
    finally:
        connection.close()
