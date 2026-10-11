
import os
import sys
import json
import certifi
import pandas as pd
import pymongo

from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger

load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URL")
CA_FILE = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            if not MONGO_DB_URL:
                raise ValueError("MONGODB_URL is missing from .env")

            self.client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=CA_FILE,
                serverSelectionTimeoutMS=10000
            )

            # Verify the connection
            self.client.admin.command("ping")

            self.db = self.client["network_security"]
            self.collection = self.db["network_data"]

            logger.info("MongoDB Atlas connection successful")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json(self, csv_file_path):
        try:
            df = pd.read_csv(csv_file_path)
            df.reset_index(drop=True, inplace=True)

            json_data = json.loads(df.T.to_json())
            return list(json_data.values())

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, json_data, database, collection):
        try:
            target_collection = self.client[database][collection]

            if not json_data:
                logger.warning("No records found to insert")
                return 0

            result = target_collection.insert_many(json_data)

            logger.info(
                f"Inserted {len(result.inserted_ids)} records "
                f"into {database}.{collection}"
            )

            return len(result.inserted_ids)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        FILE_PATH = r"Network_Data\phisingData.csv"
        DATABASE = "Vivek"
        COLLECTION = "Network_Data"

        network_obj = NetworkDataExtract()

        records = network_obj.csv_to_json(file_path=FILE_PATH)

        no_of_records = network_obj.insert_data_mongodb(
            records,
            DATABASE,
            COLLECTION
        )

        print(
            f"{no_of_records} records inserted successfully into "
            f"{DATABASE}.{COLLECTION}."
        )

    except Exception as e:
        print(f"Data upload failed: {e}")
        raise

    finally:
        if "network_obj" in locals():
            network_obj.client.close()
