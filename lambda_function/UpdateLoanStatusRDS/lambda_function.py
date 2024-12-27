import pymysql

def lambda_handler(event, context):
    try:
        # Extract input data
        loan_id = event.get("loan_id", "")
        answer = event.get("answer", "")
        loan_officer_id = event.get("loan_officer_id", "")

        # Input validation
        if not loan_id or not answer or not loan_officer_id:
            return {
                "statusCode": 400,
                "error": "loan_id, answer, and loan_officer_id are required"
            }

    except Exception as e:
        return {
            "statusCode": 400,
            "error": f"Invalid input data: {str(e)}"
        }

    try:
        # Establish a connection to the RDS database
        connection = pymysql.connect(
            host='database-1.cd0keqmiesi5.us-east-1.rds.amazonaws.com',
            user='admin',
            password='GvUFyayd)42Q8tgnguknBNCJ<QTQ',
            database='users-info',
            port=3306
        )

        with connection.cursor() as cursor:
            # Update the loan's answer and loan_officer based on loan_id
            update_query = """
                UPDATE loans 
                SET answer = %s, loan_officer_id = %s
                WHERE loan_id = %s
            """
            cursor.execute(update_query, (answer, loan_officer_id, loan_id))
            connection.commit()

        return {
            "statusCode": 200,
            "message": f"Loan with ID {loan_id} successfully updated with answer '{answer}' by loan officer '{loan_officer_id}'"
        }

    except pymysql.MySQLError as e:
        return {
            "statusCode": 500,
            "error": f"Database error: {str(e)}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"An unexpected error occurred: {str(e)}"
        }
    finally:
        if 'connection' in locals():
            connection.close()

