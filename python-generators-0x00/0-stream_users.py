#!/usr/bin/python3
"""
Module for streaming user data from MySQL database using generators.
"""
import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that fetches rows one by one from the user_data table.
    
    Yields:
        dict: A dictionary containing user data with keys:
              user_id, name, email, age
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Security@123',
            database='ALX_prodev'
        )
        
        # Create cursor with dictionary=True to get results as dictionaries
        cursor = connection.cursor(dictionary=True)
        
        # Execute query to fetch all users
        cursor.execute("SELECT * FROM user_data")
        
        # Fetch and yield one row at a time
        for row in cursor:
            yield row
        
        # Clean up
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error: {e}")