def test_DB(db):
    try:
        # Delete all documents in the collection, just for caution
        db.clean_device_plant()

        # Insert new data
        db.insert_into_device_plant("1", 1, 1, 1)
        db.insert_into_device_plant("2", 2, 2, 2)

        # Find device 2
        result = db.find_in_device_plant("2")
        print(result)

        # Time to check!
        input("Check on your DBMS if the commited changes are reflected! Type anything when you're ready, and those changes will be deleted: ")

    except Exception as e:
        print(e)

    finally:
        # Delete all documents in the collection
        db.clean_device_plant()

        db.shutdown()