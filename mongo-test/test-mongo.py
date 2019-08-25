from pymongo import MongoClient
import logging
import sys
from config.mongodb import mongo_config


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
        db = client[mongo_config()['database']]
        print(db.name)
        predictions = db['reefer_container_predictions']
        prediction_row = {'id': 1234,
                          'maintenance_required': 'true'}
        logging.debug(prediction_row)
        predictions.insert_one(prediction_row)

    except Exception as err:
        logging.error(err)
    finally:
        client.close()

if __name__ == '__main__':
    main()