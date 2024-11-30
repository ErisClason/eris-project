import psycopg2

# Connection parameters
DB_HOST = "localhost"  # 'localhost' assumes the database is on the same machine
DB_PORT = "5432"       # Default PostgreSQL port
DB_USER = "postgres"   # Default superuser
DB_PASSWORD = "dpPoZSc6r7zy6kpszr3Vd4EuUSbfp576"  # Your database password
DB_NAME = "postgres"   # Default database name

try:
    # Establishing connection
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    print("Connection successful!")
    
    # Fetch PostgreSQL version
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"An error occurred: {e}")
