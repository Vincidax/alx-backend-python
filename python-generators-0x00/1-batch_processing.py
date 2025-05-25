#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches user_data rows from DB in batches of size batch_size.
    Each batch is a list of dicts.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
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
                break
            yield batch
            offset += batch_size
        
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

def batch_processing(batch_size):
    """
    Processes batches from stream_users_in_batches, yields only users older than 25.
    """
    # Loop 1: Iterate over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: Iterate over each user in batch
        for user in batch:
            # Loop 3: condition check inside loop (not an explicit loop)
            if user['age'] > 25:
                yield user
