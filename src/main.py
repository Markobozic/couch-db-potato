import argparse
from src.importer import CouchImporter


def main():

    couchdb_default_url = 'localhost'
    couchdb_default_creds = ''
    couchdb_default_port = 5984
    csv_default_path = ''
    couchdb_default_doc_qty = 20000

    parser = argparse.ArgumentParser()

    parser.add_argument('-f',
                        '--file',
                        help="The path to the csv file",
                        type=str)

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

    parser.add_argument('-c',
                        '--creds',
                        help="The username and password for couchDB server with permissions to add/edit.",
                        type=str)

    parser.add_argument('-q',
                        '--docqty',
                        help="The number of documents to upload at a time",
                        type=int)

    args = parser.parse_args()

    if args.file is not None:
        couchdb_default_path = args.file

    if args.url is not None:
        couchdb_default_url = args.url

    if args.port is not None:
        couchdb_default_port = args.port

    if args.creds is not None:
        couchdb_default_creds = args.creds

    if args.docqty is not None:
        couchdb_default_doc_qty = args.docqty

    database_name = args.database_name

    db = CouchImporter(couchdb_default_url,
                       couchdb_default_port,
                       csv_default_path,
                       database_name,
                       couchdb_default_creds,
                       couchdb_default_doc_qty)

    db.import_to_couchdb()

if __name__ == '__main__':
    main()
