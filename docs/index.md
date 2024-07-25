# data-api-template

## Purpose

Simplon wants to create a database to compare its training offering with those of other training centers. This will allow employees to understand which training courses face strong competition and will offer potential learners alternatives if Simplon training courses are complete. 

We will:

- Scrape the Simplon site and use moncompteformation BDD to create a database.
- The API will allow Simplon to search for competing courses based on two criteria: region and formacode.
- The API will be developed with FastAPI, dockerized, and deployed on Azure ACI.
- A Streamlit dashboard to expose API results.

read the full documentation: [here](https://charles-42.github.io/ml-model-api-template/)

## Dependencies:
- poetry
- geopy

## Setup

1. Create virtual environement and install requierements:

```bash

poetry install

```

2. Create .env file using env_template.txt


3. To create the Olist database, execute these commands:

```bash
chmod +x ./database/azure_postgres/create_postgres.sh
./database/azure_postgres/create_postgres.sh

chmod +x ./database/azure_postgres/create_tables.sh
./database/azure_postgres/create_tables.sh

chmod +x ./database/azure_postgres/import_postgres.sh
./database/azure_postgres/import_postgres.sh
```

4. You can execute tests to make sure the setup is good:

```bash
pytest
```
## Train a new model

You can update training functions and then use ./model/train.sh to train a new model. (Don't forget to change run_name)

## Launch the API

1. Get your token:

```bash
poetry run python -m api.utils
```

2. Update model_name in ./api/launch_app.sh and then you can execute it

## Use Streamlit ML-OPS Dashboard

Execute this command

```bash
poetry run streamlit run ml_ops/dashboard.py
```