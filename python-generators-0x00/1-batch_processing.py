#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from the user_data table.
    
    Args:
        batch_size (int): Number of rows to fetch per batch
    
    Yields:
        list: A list of dictionaries, each containing user data with keys:
              user_id, name, email, age
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        
        # Create cursor with dictionary=True to get results as dictionaries
        cursor = connection.cursor(dictionary=True)
        
        # Execute query to fetch all users
        cursor.execute("SELECT * FROM user_data")
        
        # Fetch and yield batches (Loop 1)
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    
    Args:
        batch_size (int): Number of rows to fetch per batch
    
    Prints:
        Filtered user data for users over age 25
    """
    # Get batches from the generator (Loop 2)
    for batch in stream_users_in_batches(batch_size):
        # Filter users over age 25 in each batch (Loop 3)
        for user in batch:
            if user['age'] > 25:
                print(user)