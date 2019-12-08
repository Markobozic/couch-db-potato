import csv
import json
import requests
import pandas as pd
import simplejson
import time


class CouchImporter:

    def __init__(self, base_url, port, csv_path, database_name):
        self.start_time = time.time()
        self.base_url = base_url
        self.port = port
        self.admin_creds = 'admin:project3'
        self.url = f'http://{self.admin_creds}@{base_url}:{port}'
        self.database_name = database_name
        self.csv_path = csv_path
        self.csv_line_counter = 0
        self.document_count = 0
        self.document_list = []
        self.maximum_documents_to_bulk_load = 50000
        
        self.bulk_doc_to_load = {
            "docs": []
        }

    def test_couchdb_connection(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions:
            print(f'The database connection for {self.url} could not be established. Verify that CouchDB is running')

    def create_database_if_nonexistent(self):
        try:
            response = requests.get(f'{self.url}/{self.database_name}')
            response.raise_for_status()
        except Exception:
            print(f'The database {self.database_name} does not exist ... creating it now.')
            response = requests.put(f'{self.url}/{self.database_name}')
            print(f'Database {self.database_name} created.')

    def import_to_couchdb(self):
        self.test_couchdb_connection()
        self.create_database_if_nonexistent()

        print("Reading CSV Files")

        detectors = pd.read_csv('src/freeway_detectors.csv', usecols= ["detectorid","stationid","detectorclass","lanenumber"])
        stations = pd.read_csv('src/freeway_stations.csv')
        highways = pd.read_csv('src/highways.csv')
        loopdata = pd.read_csv('src/freeway_loopdata.csv')

        print("Joining CSV Files")

        merged = detectors.merge(stations.merge(highways, how='left', on='highwayid'), how='left', on='stationid')
        merged_loop_data = loopdata.merge(merged, how='left', on='detectorid')

        print("Loading Detector Documents")

        #This section loads detectors one by one. Since there are only around 50 this is okay and doesn't take very long
        def load_detectors(row):
            stations = row[['stationid','upstream','downstream','stationclass','numberlanes','latlon','length']]
            highways = row[['highwayid','shortdirection','direction','highwayname']]
            detectors = row[['detectorid','milepost','locationtext','detectorclass','lanenumber']]

            data = detectors.to_dict()
            data["docType"] = 'detector'
            data["station"] = stations.to_dict()
            data["highway"] = highways.to_dict()

            doc_id = detectors[['detectorid']].to_string(index=False).strip()
            url = f'{self.url}/{self.database_name}/' + doc_id

            json_data = json.dumps(data)
            response = requests.put(url, data=json_data, headers={'Content-Type': 'application/json'})

        merged.apply(lambda x: load_detectors(x), axis=1)

        print("Preparing Loop Documents")

        for index, row in merged_loop_data.iterrows():

            document = {}

            # We don't want detectors with speed 0
            if row['speed'] == '0':
                continue

            document['_id'] = str(row['detectorid']) + '_' + row['starttime']
            document['starttime'] = row['starttime']
            document['volume'] = row['volume']
            document['speed'] = row['speed']
            document['occupancy'] = row['occupancy']
            document['status'] = row['status']
            document['detectorid'] = row['detectorid']
            document['length'] = row['length']
            document['locationtext'] = row['locationtext']
            

            self.document_list.append(document)
            self.csv_line_counter += 1
            self.document_count += 1

            if self.document_count == self.maximum_documents_to_bulk_load:
                    self.bulk_doc_to_load['docs'] = self.document_list
                    self.bulk_upload_documents_to_couchdb()
                    self.cleanup()

    def bulk_upload_documents_to_couchdb(self):
        try:
            response = requests.post(f'{self.url}/{self.database_name}/_bulk_docs',
                                     data=simplejson.dumps(self.bulk_doc_to_load, ignore_nan=True),
                                     headers={'Content-type': 'application/json'})
            response.raise_for_status()
        except Exception as err:
            print(f'Error trying to load documents to CouchDB: {err}')

    def cleanup(self):
        self.document_list = []
        self.bulk_doc_to_load['docs'] = []
        self.document_count = 0
        elapsed_time = time.time() -self.start_time
        print(f'Bulk uploading {self.maximum_documents_to_bulk_load} documents, current document count is {self.csv_line_counter} - ', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), end="\r")