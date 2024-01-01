import os
from dotenv import load_dotenv
import psycopg2 as pg

from database import Database

class Postgres(Database):

    def __init__(self):
        load_dotenv()

        self.USER = os.getenv('POSTGRES_USER')
        self.PASSWORD = os.getenv('POSTGRES_PASSWORD')
        self.DB = os.getenv('POSTGRES_DB')

        # Connect to the POSTGRES_DB database
        self.conn = pg.connect(database=self.DB, user=self.USER, password=self.PASSWORD)

    def shutdown(self):
        self.conn.close()

    def insert_into_device_plant(self, id_device, id_plant, plant_type, id_user):
        cursor = self.conn.cursor()

        insert_query = "INSERT INTO dev.device_plant(id_device, id_plant, plant_type, id_user) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (id_device, id_plant, plant_type, id_user))

        self.conn.commit()
        cursor.close()

    def find_in_device_plant(self, id_device):
        cursor = self.conn.cursor()

        find_query = """SELECT * FROM dev.device_plant 
                            WHERE id_device = %s"""
        cursor.execute(find_query, (id_device,))
        result = cursor.fetchone()

        cursor.close()
        return {
            "id_device": result[0],
            "id_plant": result[1],
            "plant_type": result[2],
            "id_user": result[3],
        }
    
    def clean_device_plant(self):
        cursor = self.conn.cursor()

        cursor.execute(f"DELETE FROM dev.device_plant")
        self.conn.commit()

        cursor.close()