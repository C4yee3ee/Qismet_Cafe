import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'qismet_cafe',
    'raise_on_warnings': True
}

def connect():
    """Establishes and returns a connection to the MySQL database."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise Exception("Access denied: Check your database username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise Exception("Database does not exist: Check the database name.")
        else:
            raise Exception(f"Database connection failed: {err}")

if __name__ == "__main__":
    try:
        conn = connect()
        print("Successfully connected to the database!")
        conn.close()
    except Exception as e:
        print(f"Connection test failed: {e}")