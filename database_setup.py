import psycopg2

def test_connection():
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname="hardware_project", 
            user="postgres", 
            password="postgres", 
            host="localhost", 
            port="5432"
        )
        print("✅ Connection Successful! You are officially a DBA in the making.")
        conn.close()
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()