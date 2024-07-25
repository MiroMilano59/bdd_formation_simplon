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
