import csv
import json
import requests
import pandas as pd


class CouchImporter:

    def __init__(self, base_url, port, csv_path, database_name):
        self.base_url = base_url
        self.port = port
        self.url = f'http://{base_url}:{port}'
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
            requests.put(f'{self.url}/{self.database_name}')
            print(f'Database {self.database_name} created.')

    def import_detectors_to_couchdb(self):
        self.test_couchdb_connection()
        self.create_database_if_nonexistent()

        detectors = pd.read_csv('freeway_detectors.csv', usecols= ["detectorid","stationid","detectorclass","lanenumber"])
        stations = pd.read_csv('freeway_stations.csv')
        highways = pd.read_csv('highways.csv')

        merged = detectors.merge(stations.merge(highways, how='left', on='highwayid'), how='left', on='stationid')

        def loadrow(row):
            stations = row[['stationid','upstream','downstream','stationclass','numberlanes','latlon','length']]
            highways = row[['highwayid','shortdirection','direction','highwayname']]
            detectors = row[['detectorid','milepost','locationtext','detectorclass','lanenumber']]

            data = detectors.to_dict()
            data["docTypec"] = 'detector'
            data["station"] = stations.to_dict()
            data["highway"] = highways.to_dict()

            url = detectors[['detectorid']].to_string(index=False).strip()
            url = f'{self.url}/{self.database_name}/' + url

            json_data = json.dumps(data)
            response = requests.put(url, data=json_data, headers={'Content-Type': 'application/json'})

        merged.apply(lambda x: loadrow(x), axis=1)
        self.cleanup()

    def import_csv_to_couchdb(self):

        self.test_couchdb_connection()
        self.create_database_if_nonexistent()

        with open(self.csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:

                # This is the column names we don't want uploaded
                if self.csv_line_counter == 0:
                    self.csv_line_counter += 1
                    continue

                document = {}

                # We don't want detectors with speed 0
                if row[3] == '0':
                    continue

                datetime = row[1].replace(' ', '_')

                document['_id'] = f'{row[0]}_{datetime}'
                document['docType'] = 'loop'
                document['starttime'] = row[1]
                document['volume'] = row[2]
                document['speed'] = row[3]
                document['occupancy'] = row[4]
                document['status'] = row[5]
                document['detectorid'] = row[0]

                self.document_list.append(document)
                self.csv_line_counter += 1
                self.document_count += 1

                if self.document_count == self.maximum_documents_to_bulk_load:
                    print(f'Bulk uploading 50000 documents, current document count is {self.csv_line_counter}')
                    self.bulk_doc_to_load['docs'] = self.document_list
                    self.bulk_upload_documents_to_couchdb()
                    self.cleanup()

    def bulk_upload_documents_to_couchdb(self):
        try:
            response = requests.post(f'{self.url}/{self.database_name}/_bulk_docs',
                                     data=json.dumps(self.bulk_doc_to_load),
                                     headers={'Content-type': 'application/json'})
            response.raise_for_status()
        except Exception as err:
            print(f'Error trying to load documents to CouchDB: {err}')

    def cleanup(self):
        self.document_list = []
        self.bulk_doc_to_load['docs'] = []
        self.document_count = 0







