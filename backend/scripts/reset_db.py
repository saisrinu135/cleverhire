import psycopg2
import os
import sys

# Load env variables directly since django setup might fail if DB is bad
def get_env_var(name, default):
    # Simple parser for .env
    try:
        with open('../.env', 'r') as f:
            for line in f:
                if line.startswith(name + '='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return os.environ.get(name, default)

DB_NAME = get_env_var('DB_NAME', 'cleverhire')
DB_USER = get_env_var('DB_USER', 'cleverhire')
DB_PASSWORD = get_env_var('DB_PASSWORD', 'cleverhire')
DB_HOST = get_env_var('DB_HOST', 'localhost')
DB_PORT = get_env_var('DB_PORT', '5432')

print(f"Connecting to {DB_NAME} as {DB_USER}...")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.set_isolation_level(0) # Autocommit
    cur = conn.cursor()
    
    print("Dropping public schema...")
    cur.execute("DROP SCHEMA public CASCADE;")
    print("Recreating public schema...")
    cur.execute("CREATE SCHEMA public;")
    print("Granting permissions...")
    cur.execute(f"GRANT ALL ON SCHEMA public TO {DB_USER};")
    cur.execute(f"GRANT ALL ON SCHEMA public TO public;")
    
    # Enable PostGIS extension again if it was dropped (extensions usually in public)
    print("Enabling PostGIS...")
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    except Exception as e:
        print(f"Warning explicitly enabling postgis: {e}")
        # Might need superuser for this, but if extension was installed in another schema or if user is superuser it works.
        
    cur.close()
    conn.close()
    print("Database reset successfully.")
except Exception as e:
    print(f"Error resetting database: {e}")
    sys.exit(1)
