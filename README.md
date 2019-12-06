# couch-db-potato

## Uploading the loop data

The program runs from `main.py`. It takes 4 arguements, 2 required, 2 optional.

### Arguments:

`-f path-to-your-csv-file.csv` -- this is REQUIRED, the path to the csv file from the directory you're running.
`-d your-database-name` -- this is REQUIRED, the name of the database, if it doesn't exist the app will create it for you
`-u url-where-couchdb-is-running` -- this is OPTIONAL, it will default to `localhost` 
`-p port-couchdb-is-running-on` -- this is OPTIONAL, it will default to `5984`

Python is notorious for import problems, if you see an error like `Cannot find module 'src'` or similar try:
```
export PYTHONPATH="${PYTHONPATH}:path/to/couch-db-potato-directory/"
```

For instance this project for me is located at `/Users/Marko/code/couch-db-potato`, so i would type in my shell:

`export PYTHONPATH="${PYTHONPATH}:/Users/Marko/code/couch-db-potato"`

## Running the application

Running the app looks something like `python3 main.py -f /Users/Marko/code/loop_data.csv -d loop_database` 
