import argparse
from src.importer import CouchImporter


def main():

    couchdb_default_url = 'localhost'
    couchdb_default_port = 5984

    parser = argparse.ArgumentParser()

    parser.add_argument('-f',
                        '--file',
                        help="The path to the csv file",
                        type=str,
                        required=True)

    parser.add_argument('-d',
                        '--database_name',
                        help="The name of the CouchDB database",
                        type=str,
                        required=True)

    parser.add_argument('-u',
                        '--url',
                        help="The url to the CouchDB server",
                        type=str)

    parser.add_argument('-p',
                        '--port',
                        help="The port your CouchDB instance is running on",
                        type=str)

    args = parser.parse_args()
    csv_file_path = args.file
    database_name = args.database_name

    if args.url is not None:
        couchdb_default_url = args.url

    if args.port is not None:
        couchdb_default_port = args.port

    db = CouchImporter(couchdb_default_url,
                       couchdb_default_port,
                       csv_file_path,
                       database_name)

    db.import_detectors_to_couchdb()
    db.import_csv_to_couchdb()


if __name__ == '__main__':
    main()
