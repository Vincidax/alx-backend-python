#!/usr/bin/python3
import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to the MySQL server."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      # change if needed
            password="",      # add password if needed
            database="ALX_prodev"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, csv_file):
    """Insert data from CSV into user_data table if user_id not already present."""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Assuming CSV has columns: user_id, name, email, age
                user_id = row['user_id']
                name = row['name']
                email = row['email']
                age = row['age']

                # Check if user_id exists
                cursor.execute("SELECT COUNT(*) FROM user_data WHERE user_id = %s", (user_id,))
                exists = cursor.fetchone()[0]

                if exists == 0:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )
        connection.commit()
        cursor.close()
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
