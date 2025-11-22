# Inventory Management System (Summative)

A simple Python + Flask project that manages an inventory of products. 
This project includes: 

- A Flask API (GET, POST, PATCH, DELETE)
- An external API integration (OpenFoodFacts barcode lookup)
- A command-line interface (CLI)
- Automated tests using pytest


## Features

**Flask API**

- GET /inventory - list all items
- GET /inventory/<id> - get one item
- POST /inventory - add a new item
- PATCH /inventory/<id> - update an item
- DELETE / inventory/<id> - delete an item
- POST / inventory/from-barcode - create an item using a barcode lookup


## External API

Uses OpenFoodFacts to fetch:

- product name
- brand
- ingredients


## Command-Line Interface (CLI)

Run:

```
python3 cli.py
```

You can:

- View all items
- Look up an item by ID
- Add a new item


## How to run the Server

```
python3 app.py
```
Flask will start at: http://127.0.0.1:5000


## Running Tests

```
pytest
```

