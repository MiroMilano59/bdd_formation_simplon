import pandas as pd
from BDD import models, crud

# BASIC SETTINGS & INITIALIZATION
file = "TRAITEMENT_MCF\SRC\data_formation.json"  # Path to the most recent json
simplon = '79279132900016'                       # SIRET of "simplon.co"
data_dtypes = {'siret': str,                     # To manage json data types
               'code_inventaire': str,
               'code_rncp': str}
data_dtypes.update({f"code_nsf_{i}": str for i in range(1,4)})
data_dtypes.update({f"code_formacode_{i}": str for i in range(1,6)})

# DATA LOADING & SAVING (i.e. filling the 'simplon' database with the data)
# 1. Whole process scheduler
def load_data():
    """
    Open a '.json' file (from `moncompteformation`) and save data in database.

    No parameters and nothing returned (just data added to thedatabase)
    """

    # DATA SAVING PROCESS
    data = get_dataframe()                                     # Open json file
    session = get_session()
    save_organizations_to_database(data=data, session=session)
    save_trainings_to_database(data=data, session=session)

# 2. Underlying features
def get_dataframe():
    """
    Open the `.json` file and returns a dataframe. No arguments required.
    """

    # CHANGES JSON SOURCE FILE INTO A DATAFRAME
    data = pd.read_json(file, dtype=data_dtypes) # Read the json file

    # DROPS SIMPLON ROWS (since simplon data are retrieved by scraping way)
    data['siret'] = data['siret'].str.strip()    # Pre-cleaning to be 100% sure
    data = data[data['siret'] != simplon]        # Drops simplon siret rows

    # FUNCTION OUTPUT
    return data

def save_organizations_to_database(data, session=None):
    """
    Retrieves organisations data and updates the dedidacted table in database.

    Parameter(s):
        data    : Pandas dataframe with 'siret' and 'nom_of' columns.
        session : OPTIONAL. 'session' object to connect the database.
                  For any details see SQLAlchemy documentation.
    """

    # GETS ALL UNKNOWN SIRET
    siret = set(data['siret'].unique()) - crud.get_siret()

    # EXTRACT UNKNOWN ORGANIZATIONS (select relevant fields + drop duplicates)
    if len(siret) > 0:
        # Selects relevant data only (i.e. name and siret where siret unknown)
        orgz = data[['siret', 'nom_of']][data['siret'].isin(siret)]

        # Keeps only one copy for each new case (i.e. drops duplicates) 
        orgz = orgz.drop_duplicates().to_numpy()

        # First creates dictionnaries with data then instances of `Organismes`
        orgz = [{'Siret': siret, 'Nom': name} for siret, name in orgz]
        orgz = [models.Organismes(**company) for company in orgz]

        # Adds all new instances in the database at once
        crud.add_and_commit(orgz)

def save_trainings_to_database(data, session=None):
    """
    Retrieves organisations data and updates the dedidacted table in database.

    Parameter(s):
        data    : Pandas dataframe with 'siret' and 'intitule_certification'.
        session : OPTIONAL. 'session' object to connect the database.
                  For any details see SQLAlchemy documentation.
    """

    # GETS ALL UNKNOWN SIRET
    # siret = set(data['siret'].unique()) - crud.get_siret()
    pass

# DATABASE CONNECTION FEATURE
def get_session():
    """Helper function which returns a ready-to-use connection to the database.

    Needs no arguments. Returns a session object (see SQLAlchemy for details).
    """

    session = models.db_connect()
    return session()


if __name__ == "__main__":
    save_organizations_to_database(get_dataframe())