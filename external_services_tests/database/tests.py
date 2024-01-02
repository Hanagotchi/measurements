from datetime import datetime
from sql_alchemy import SQL_Alchemy, DevicePlant, Measurement

def test_DB_device_plant(db: SQL_Alchemy):
    try:
        # Delete all documents in the collection, just for caution
        db.clean_table(DevicePlant)

        # Insert new data

        DevicePlant(
            id_device="1",
            id_plant=2,
            plant_type=2,
            id_user=2,
        )
        db.add_new(DevicePlant(id_device="1", id_plant=1, plant_type=1, id_user=1))
        db.add_new(DevicePlant(id_device="2", id_plant=2, plant_type=2, id_user=2))

        # Find device 2
        result = db.find_device_plant("2")
        assert(result.id_device == "2" and result.id_plant == 2 and result.plant_type == 2 and result.id_user == 2)
        print(result)

        # Update device 2
        db.update_device_plant("2", 3, None, 3)
        result: DevicePlant = db.find_device_plant("2")
        assert(result.id_device == "2" and result.id_plant == 3 and result.plant_type == 2 and result.id_user == 3)
        print(result)

        # Time to check!
        input("Check on your DBMS if the commited changes are reflected! Type anything when you're ready, and those changes will be deleted: ")
    
    except Exception as e:
        print(f"ERROR: {e}")

    finally:
        # Delete all documents in the collection
        db.clean_table(DevicePlant)
        db.shutdown()

def test_DB_measurements(db: SQL_Alchemy):
    try:
        # Delete all documents in the collection, just for caution
        db.clean_table(Measurement)


        # Insert random data
        for i in range(1, 6):
            db.add_new(Measurement(id_plant=1, 
                                   plant_type=12, 
                                   time_stamp=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), 
                                   temperature=i, 
                                   humidity=i,
                                   light=i,
                                   watering=i))
            
        for i in range(6, 1, -1):
            db.add_new(Measurement(id_plant=2, 
                                   plant_type=6, 
                                   time_stamp=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), 
                                   temperature=i, 
                                   humidity=i,
                                   light=i,
                                   watering=i))
            
        for i in range(4, 20, 2):
            db.add_new(Measurement(id_plant=3, 
                                   plant_type=9, 
                                   time_stamp=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), 
                                   temperature=i, 
                                   humidity=i,
                                   light=i,
                                   watering=i))

        # Find last insertion
        result = db.get_last_measurement(2)
        assert(result.temperature == 2)
        print(result)

        # Time to check!
        input("Check on your DBMS if the commited changes are reflected! Type anything when you're ready, and those changes will be deleted: ")
    
    except Exception as e:
        print(f"ERROR: {e}")

    finally:
        # Delete all documents in the collection
        db.clean_table(Measurement)
        db.shutdown()