#!/usr/bin/env python3
"""
Script to set up MySQL database ALX_prodev with user_data table
and populate it with sample data from CSV file.
"""
import mysql.connector
from mysql.connector import Error
import csv
import uuid
import os


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='Security@123'   
        )
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully or already exists")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        connection: MySQL connection object connected to ALX_prodev or None
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',      
            password='Security@123',      
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Successfully connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates the user_data table if it does not exist with required fields.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5, 2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully or already exists")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, data):
    """
    Inserts data into the database if it does not exist.
    
    Args:
        connection: MySQL connection object
        data: Tuple containing (user_id, name, email, age)
    """
    try:
        cursor = connection.cursor()
        
        # Check if user already exists
        check_query = "SELECT user_id FROM user_data WHERE user_id = %s"
        cursor.execute(check_query, (data[0],))
        
        if cursor.fetchone() is None:
            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, data)
            connection.commit()
            print(f"Inserted data for user: {data[1]}")
        else:
            print(f"User {data[1]} already exists, skipping...")
        
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")


def stream_users_from_csv(csv_file):
    """
    Generator function that streams rows from CSV file one by one.
    
    Args:
        csv_file: Path to the CSV file
        
    Yields:
        tuple: (user_id, name, email, age)
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate UUID for user_id if not present
                user_id = row.get('user_id', str(uuid.uuid4()))
                name = row.get('name', '')
                email = row.get('email', '')
                age = row.get('age', 0)
                
                yield (user_id, name, email, age)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found")
    except Exception as e:
        print(f"Error reading CSV file: {e}")


def main():
    """
    Main function to set up database and populate with data.
    """
    # Step 1: Connect to MySQL server
    connection = connect_db()
    if not connection:
        return
    
    # Step 2: Create database
    create_database(connection)
    connection.close()
    
    # Step 3: Connect to ALX_prodev database
    db_connection = connect_to_prodev()
    if not db_connection:
        return
    
    # Step 4: Create table
    create_table(db_connection)
    
    # Step 5: Load data from CSV using generator
    csv_file = 'user-data.csv'
    
    if os.path.exists(csv_file):
        print(f"\nLoading data from {csv_file}...")
        user_generator = stream_users_from_csv(csv_file)
        
        # Insert data using generator
        for user_data in user_generator:
            insert_data(db_connection, user_data)
        
        print("\nData loading complete!")
    else:
        print(f"\nWarning: {csv_file} not found. Please ensure the file exists.")
        print("Creating sample data instead...")
        
        # Insert sample data if CSV not found
        sample_data = [
            (str(uuid.uuid4()), 'John Doe', 'john.doe@example.com', 30.00),
            (str(uuid.uuid4()), 'Jane Smith', 'jane.smith@example.com', 25.50),
            (str(uuid.uuid4()), 'Bob Johnson', 'bob.johnson@example.com', 35.75)
        ]
        
        for data in sample_data:
            insert_data(db_connection, data)
    
    # Close connection
    db_connection.close()
    print("\nDatabase setup completed successfully!")


if __name__ == "__main__":
    main()