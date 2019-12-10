# couch-db-potato

## Uploading the loop data

The program runs from `main.py`. It takes 4 arguments, 2 required, 2 optional.

### Arguments:

(OPTIONAL) `-f path-to-your-csv-file.csv` -- the path to the csv files from the directory you're running. -- it will default to program directory <br/>
(REQUIRED) `-d your-database-name` -- the name of the database, if it doesn't exist the app will create it for you. May need admin credentials for it to work. <br/>
(OPTIONAL) `-u url-where-couchdb-is-running` -- it will default to `localhost` <br/>
(OPTIONAL) `-p port-couchdb-is-running-on` -- it will default to `5984` <br/>
(OPTIONAL) `-c credentials in username:password format` with permissions to add databases, design documents. <br/>
(OPTIONAL) `-q quantity of documents to upload at a time` -- it will default to `20000`

Python is notorious for import problems, if you see an error like `Cannot find module 'src'` or similar try:
```
export PYTHONPATH="${PYTHONPATH}:path/to/couch-db-potato-directory/"
```

For instance this project for me is located at `/Users/Marko/code/couch-db-potato`, so i would type in my shell:

`export PYTHONPATH="${PYTHONPATH}:/Users/Marko/code/couch-db-potato"`

## CSV files
The program will look for the detector, station, highway, and loop data csv files in the src folder. Make sure they are there before running. The file names should match
the file names in importer.py and if you move the files somewhere else you must supply the -f paramater with the path to the csv files.

## Running the application

Running the app looks something like `python3 main.py -d freeway -u 35.233.160.123 -c admin:project3` 
