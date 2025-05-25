#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of user rows from user_data table.
    Each batch is a list of dictionaries.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # adjust if needed
            password="",       # adjust if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        
        offset = 0
        while True:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data "
                "LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                return  # cleanly end generator when no more rows
            yield batch
            offset += batch_size
        
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return  # end generator on error

def batch_processing(batch_size):
    """
    Generator that yields users over age 25 from batches.
    """
    # Loop 1: iterate over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: iterate over each user in batch
        for user in batch:
            if user['age'] > 25:
                yield user
    return  # explicitly end generator
