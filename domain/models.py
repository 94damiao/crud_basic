import mysql.connector
from mysql.connector import Error
import os

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "username"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_NAME", "dbname")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"The error '{e}' occurred")
    return None

def execute_query(query, params=None):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    result = []
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if cursor.with_rows:
            result = cursor.fetchall()
        else:
            connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()
    return result