import pandas as pd
from BDD import models, crud

# BASIC SETTINGS & INITIALIZATION
file = "TRAITEMENT_MCF\SRC\data_formation.json"  # Path to the most recent json
simplon = '79279132900016'                       # SIRET of "simplon.co"
data_dtypes = {'siret': str}                     # To manage json data types 

# DATA LOADING & SAVING (i.e. filling the 'simplon' database with the data)
# 1. Whole process scheduler
def load_data():
    """
    Open a '.json' file (from `moncompteformation`) and save data in database.

    No parameters and nothing returned (just data added to thedatabase)
    """

    # CHANGES JSON SOURCE FILE INTO A DATAFRAME
    data = pd.read_json(file, dtype=data_dtypes)         # Read the json file

    # DROPS SIMPLON ROWS (since simplon data are retrieved by scraping way)
    data['siret'] = data['siret'].str.strip()    # Pre-cleaning to be 100% sure
    data = data[data['siret'] != simplon]        # Drops simplon rows

    # DATA SAVING PROCESS
    session = get_session()
    save_organizations_to_database(data=data, session=session)

# 2. Underlying features
def save_organizations_to_database(data, session=None):
    """
    Retrieves organisations data and updates the dedidacted table in database.

    Parameter(s):
        data    : Pandas dataframe with 'siret' and 'nom_of' columns.
        session : OPTIONAL. 'session' object to connect the database.
                  For any details see SQLAlchemy documentation.
    """
    pass

# DATABASE CONNECTION FEATURE
def get_session():
    """Helper function which returns a ready-to-use connection to the database.

    Needs no arguments. Returns a session object (see SQLAlchemy for details).
    """

    session = models.db_connect()
    return session()

load_data()