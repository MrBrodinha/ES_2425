import pymysql

def lambda_handler(event, context):
    # Database connection configuration
    db_config = {
        "host": "database-1.cd0keqmiesi5.us-east-1.rds.amazonaws.com",
        "user": "admin",
        "password": "GvUFyayd)42Q8tgnguknBNCJ<QTQ",
        "database": "users-info",
        "port": 3306
    }

    try:
        # Establish connection to the RDS database
        connection = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            port=db_config["port"]
        )

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Query to fetch all users
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

        return {
            "statusCode": 200,
            "users": users
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
