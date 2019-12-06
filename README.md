# couch-db-potato

## Uploading the loop data

The program runs from `main.py`. It takes 4 arguments, 2 required, 2 optional.

### Arguments:

REQUIRED `-f path-to-your-csv-file.csv` -- the path to the csv file from the directory you're running. \n
REQUIRED `-d your-database-name` -- the name of the database, if it doesn't exist the app will create it for you \n
OPTIONAL `-u url-where-couchdb-is-running` -- it will default to `localhost` \n
OPTIONAL `-p port-couchdb-is-running-on` -- it will default to `5984` \n

Python is notorious for import problems, if you see an error like `Cannot find module 'src'` or similar try:
```
export PYTHONPATH="${PYTHONPATH}:path/to/couch-db-potato-directory/"
```

For instance this project for me is located at `/Users/Marko/code/couch-db-potato`, so i would type in my shell:

`export PYTHONPATH="${PYTHONPATH}:/Users/Marko/code/couch-db-potato"`

## Running the application

Running the app looks something like `python3 main.py -f /Users/Marko/code/loop_data.csv -d loop_database` 
