import os
import sys
import json
import certifi
import pymongo
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGODB_URL")
print(MONGO_DB_URL)

ca=certifi.where()

import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():
    def __init__(self):
        try:
            # self.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            # self.db = self.client['network_security']
            # self.collection = self.db['network_data']
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def csv_to_json(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            json_data =list(json.loads( df.T.to_json()).values())
            return json_data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    def insert_data_mongodb(self,json_data,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.json_data=json_data
            self.mongo_client =pymongo.MongoClient(MONGO_DB_URL) 
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.json_data)
            return (len(self.json_data))   
        except Exception as e:
            raise NetworkSecurityException(e, sys)    

if __name__=="__main__":
    FILE_PATH= r"Network_Data\phisingData.csv"
    DATABASE="Vivek" 
    Collection="Network_Data"
    networkobj=NetworkDataExtract()
    records= networkobj.csv_to_json(file_path=FILE_PATH)
    no_of_records=networkobj.insert_data_mongodb(json_data=records, database=DATABASE, collection=Collection)
    print(f"{no_of_records} records inserted successfully into the {Collection} collection of {DATABASE} database.")
