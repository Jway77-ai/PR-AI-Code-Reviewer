import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve your database URL from environment variables
DATABASE_URL = os.getenv('POSTGRES_URL')

if not DATABASE_URL:
    print("Error: POSTGRES_URL is not set in the environment variables.")
    exit(1)

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(DATABASE_URL)

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Define your SQL query to fetch all content from your PR table
    query = "SELECT * FROM PR;"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Print the table content
    for row in rows:
        print(row)

except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")
finally:
    if connection:
        # Close the database connection
        cursor.close()
        connection.close()
