import os
from dotenv import load_dotenv
import psycopg2 as pg

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# Connect to the POSTGRES_DB database
conn = pg.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)

table = "dev.device_plant"

# Obtain the cursor to execute queries
cursor = conn.cursor()

try:
    # Insert new rows
    insert_query = f"INSERT INTO {table}(id_device, id_plant, plant_type, id_user) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (1,1,1,1))
    cursor.execute(insert_query, (2,2,2,1))

    # Commit changes to the DB (if not, the changes wont be stored)
    conn.commit()
except Exception as e:
    print(e)


# Fetched recent changes
cursor.execute("SELECT * FROM dev.device_plant")
rows = cursor.fetchall()
print(rows)

# Time to check!
input("Check in your DBMS if the commited changes are reflected! Type anything when you're ready, and those changes will be deleted: ")

# Clean DB
cursor.execute(f"DELETE FROM {table}")
conn.commit()

# Close connection
cursor.close()
conn.close()