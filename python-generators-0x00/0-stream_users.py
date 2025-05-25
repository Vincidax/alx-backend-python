#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that yields user_data rows one by one as dictionaries."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        for row in cursor:
            yield row

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
