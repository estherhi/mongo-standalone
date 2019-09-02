from pymongo import MongoClient
import logging
import sys
from config.mongodb import mongo_config
from random import randint
import time


def setup_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def connect_to_mongo_db():
    logging.info('Connecting to MONGODB ' + mongo_config()['connection_string'])
    client = MongoClient(mongo_config()['connection_string'])
    return client

def main():
    setup_logger()
    try:
        client = connect_to_mongo_db()
        while True:
            db = client[mongo_config()['database']]
            print("database name " + db.name)
            predictions = db['reefer_container_predictions']
            id = randint(1000, 9990)
            prediction_row = {'id': id,
                              'maintenance_required': 'true'}
            predictions.insert_one(prediction_row)
            details = predictions.find_one({'id': id})
            logging.info(details)
            time.sleep(2.5)

    except Exception as err:
        logging.error(err)
    finally:
        client.close()

if __name__ == '__main__':
    main()
