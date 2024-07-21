import inspect
import regex as re
import pandas as pd
from BDD import models, crud

# BASIC SETTINGS & INITIALIZATION
file = "TRAITEMENT_MCF/SRC/data_formation.json"  # Path to the most recent json
simplon = '79279132900016'                       # SIRET of "simplon.co"

# DATABASE CONNECTION FEATURE
def get_session():
    """Helper function which returns a ready-to-use connection to the database.

    Needs no arguments. Returns a session object (see SQLAlchemy for details).
    """

    session = models.db_connect()
    return session()

# DATA LOADING & SAVING (i.e. filling the 'simplon' database with the data)
# 1. Whole process scheduler
def load_data():
    """
    Open a '.json' file (from `moncompteformation`) and save data in database.

    No parameters and nothing returned (just data added to thedatabase)
    """

    # DATA SAVING PROCESS STEP BY STEP
    data = get_dataframe()                                     # Open json file
    session = get_session()
    save_organizations_to_database(data=data, session=session)
    save_trainings_to_database(data=data, session=session)
    save_sessions_to_database(data=data, session=session)

    # CLOSING THE SESSION
    session.close()

# 2. Core Underlying features
def save_organizations_to_database(data, session):
    """
    Retrieves organisations data and updates the dedidacted table in database.

    Parameter(s):
        data    : Pandas dataframe with 'siret' and 'nom_of' columns.
        session : OPTIONAL. 'session' object to connect the database.
                  For any details see SQLAlchemy documentation.
    """

    # BASIC SETTINGS & INITIALIZATION
    fields = {'siret': 'Siret', 'nom_of': 'Nom'}
    kwargs = {'name': 'organismes', 'index': False, 'if_exists': 'append'}

    # GETS ALL UNKNOWN SIRET
    sirets = set(data['siret'].unique()) - crud.get_siret(session=session)

    # SAVE UNKNOWN ORGANIZATIONS INTO THE DEDICATED TABLE OF THE DATABASE
    if sirets:
        print("##############################################################")
        print('DETECTED NEW SIRETS TO ADD')
        print("##############################################################")
        # KEEPS ONLY ONE COPY (i.e. only one line) OF EACH UNKNOWN ORGANIZATION
        sirets = data[fields.keys()][data['siret'].isin(sirets)]
        sirets = sirets.drop_duplicates(subset='siret').rename(columns=fields)

        # CONNECTS THE DATABASE AND NEW ORGANIZATIONS TO 'organismes' TABLE
        sirets.to_sql(con=session.get_bind(), **kwargs)

def save_trainings_to_database(data, session):
    """
    Retrieves organisations data and updates the dedidacted table in database.

    Parameter(s):
        data    : Pandas dataframe with 'siret' and 'intitule_certification'.
        session : OPTIONAL. 'session' object to connect the database.
                  For any details see SQLAlchemy documentation.
    """

    # BASIC SETTINGS & INITIALIZATION (Management of column names)
    cols = ['siret', 'intitule_certification', 'points_forts']      # Dataframe
    fields = ['Siret_OF', 'Libelle', 'Resume_Programme']            # Database

    # GETS A DICTIONARY TO SYNCHRONIZE DATABASE AND DATAFRAME COLUMNS NAME
    labels = {json_lab: model_lab for json_lab, model_lab in zip(cols, fields)}

    # GETS ALL TRAININGS ALREADY REGISTERED IN THE DATABASE
    records = crud.get_trainings(session=session)
    records = pd.DataFrame(columns=cols[:-1], data=records)

    # GETS ALL UNKNOWN TRAININGS ONLY (So performs a comparison with database)
    trainings = data[cols].drop_duplicates(subset=cols[:-1])
    trainings = pd.concat((trainings, records), axis=0, ignore_index=True)
    trainings.drop_duplicates(subset=cols[:-1], keep=False, inplace=True)

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if len(trainings) > 0:
        kwargs = {'name': 'formations', 'index': False, 'if_exists': 'append'}
        trainings.rename(columns=labels, inplace=True)
        trainings.to_sql(con=session.get_bind(), **kwargs)

def save_sessions_to_database(data, session):
    """
    Retrieves sessions data and updates the dedidacted table in database.

    Parameter(s):
        data    : Pandas dataframe with the following required columns.
                    + `siret`
                    + `intitule_certification`
                    + `code_departement`
        session : OPTIONAL. 'session' object to connect the database.
                  For any details see SQLAlchemy documentation.
    """

    
    pass
# 3. Auxiliary features (i.e. various & helper functions)
def get_dataframe(file: str = file):
    """
    Open the `.json` file and returns a dataframe. No arguments required.

    Parameter(s):
        file (str): OPTIONAL. Path to the `.json` source file.
                    By default : `TRAITEMENT_MCF/SRC/data_formation.json`
    """

    # BASIC SETTINGS & INITIALIZATION (customizing json fields data type)
    fields = ['siret', 'code_inventaire', 'code_rncp']
    data_dtypes = {field: str for field in fields}
    data_dtypes.update({f"code_nsf_{i}": str for i in range(1,4)})
    data_dtypes.update({f"code_formacode_{i}": str for i in range(1,6)})

    # LOAD THE JSON SOURCE FILE AND CHANGES IT INTO A PANDAS DATAFRAME
    data = pd.read_json(file, dtype=data_dtypes)

    # DATA CLEANING
    clean_text_columns(data)

    # REMOVES SIMPLON ROWS SINCE SIMPLON DATA ARE SCRAPED ELSEWHERE
    data.drop(index=data.index[data['siret'] == simplon], inplace=True)

    # FUNCTION OUTPUT
    return data

def clean_text_columns(data):
    """
    In-place removal of extra spaces and white characters (tab, newline, etc.)

    Parameter(s):
        data: Pandas dataframe to process with below required columns.
              Required columns:
              + `siret`
              + `nom_of`
              + `intitule_formation`
              + `points_forts`

    Returns: Nothing, the given dataframe is modified in place.
    """

    # PARSES THE ABOVE FUNCTION DOCSTRING TO GET THE LIST OF COLUMNS TO CLEAN 
    cols = get_columns_from_docstring()

    # REPLACES ANY (EXTRA) WHITE CHARACTERS (replaced by a single space)
    columns = {col: r'\s+' for col in cols} # Defines a regex for each column 
    data.replace(to_replace=columns, value=" ", regex=True, inplace=True)

    # STRIP STRINGS (removes all spaces on string sides. i.e. left and right)
    columns = {col: r'^\s*|\s*$' for col in cols}
    data.replace(to_replace=columns, value="", regex=True, inplace=True)

def get_columns_from_docstring():
    """
    Parses a docstring and returns a column list (no arguments required).

    This function purpose is to be called from/by another function.
    Once called, this function will parse the docstring of the function from
    which it is called and return a list of columns label.
    There is no magic, all column name which have to be extracted from the
    docstring must be encapsulated between kackticks.
    """

    # BASIC SETTINGS & INITIALIZATION (retrieve the docstring to be parsed)
    regex = r'(?i)(?<=\+\s`).+(?=`)'           # Regex used to get column names
    function = inspect.stack()[1].function     # Gets the calling function name
    docstring = eval(f'{function}.__doc__')    # Gets the dosctring to parse

    # FUNCTION OUTPUT
    return re.findall(regex, docstring)

if __name__ == "__main__":
    # data = get_dataframe()
    # save_organizations_to_database(data)
    # save_trainings_to_database(data)
    load_data()