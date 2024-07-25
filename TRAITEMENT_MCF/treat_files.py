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
    save_new_sessions_to_database(data=data, session=session)
    update_sessions_status_in_database(data=data, session=session)
    save_rncp_codes_to_database(data=data, session=session)
    save_rs_codes_to_database(data=data, session=session)
    save_nsf_codes_to_database(data=data, session=session)
    save_formacodes_to_database(data=data, session=session)
    update_codes_info_in_database(data=data, session=session)
    associate_trainings_and_rncp_codes(data=data, session=session)
    associate_trainings_and_formacodes(data=data, session=session)
    associate_trainings_and_rs_codes(data=data, session=session)
    associate_trainings_and_nsf_codes(data=data, session=session)
    associate_rncp_codes_and_formacodes(data=data, session=session)
    associate_rs_codes_and_formacodes(data=data, session=session)
    associate_rncp_and_nsf_codes(data=data, session=session)
    associate_rs_and_nsf_codes(data=data, session=session)

    # CLOSING THE SESSION
    session.close()

# 2. Core Underlying features
def save_organizations_to_database(data, session):
    """
    Retrieves organisations data and updates the dedidacted table in database.

    Parameter(s):
        data    : Pandas dataframe with 'siret' and 'nom_of' columns.
        session : 'session' object to connect the database.
                  For any details see SQLAlchemy documentation.
    """

    # BASIC SETTINGS & INITIALIZATION
    fields = {'siret': 'Siret', 'nom_of': 'Nom'}
    kwargs = {'name': 'organismes', 'index': False, 'if_exists': 'append'}

    # GETS ALL UNKNOWN SIRET
    sirets = set(data['siret'].unique()) - crud.get_siret(session=session)

    # SAVE UNKNOWN ORGANIZATIONS INTO THE DEDICATED TABLE OF THE DATABASE
    if sirets:
        # KEEPS ONLY ONE COPY (i.e. only one line) OF EACH UNKNOWN ORGANIZATION
        sirets = data[fields.keys()][data['siret'].isin(sirets)]
        sirets = sirets.drop_duplicates(subset='siret').rename(columns=fields)

        # CONNECTS THE DATABASE AND NEW ORGANIZATIONS TO 'organismes' TABLE
        sirets.to_sql(con=session.get_bind(), **kwargs)

def save_trainings_to_database(data, session):
    """
    Retrieves organisations data and updates the dedidacted table in database.

    Parameter(s):
        data    : Pandas dataframe with 'siret' and 'intitule_formation'.
        session : 'session' object to connect the database.
                  For any details see SQLAlchemy documentation.
    """

    # BASIC SETTINGS & INITIALIZATION (Management of column names)
    cols = ['siret', 'intitule_formation', 'points_forts']  # Dataframe columns
    fields = ['Siret_OF', 'Libelle', 'Resume_Programme']    # Database columns

    # DROP ALL DUPLICATE TRAININGS FROM THE SOURCE DATAFRAME (keeps one only!) 
    courses = data[cols].drop_duplicates(subset=cols[:-1])

    # RETRIEVES THE LISTING OF THE NON DUPLICATE TRAININGS (maybe new records!) 
    trainings = list(zip(*[courses[column] for column in cols[:-1]]))

    # GETS ALL TRAININGS ALREADY REGISTERED IN THE DATABASE (to compare)
    records = crud.get_trainings(session=session)

    # LOCATES NEW TRAININGS TO SAVE AND DEDUCES INDEXES TO DROP FROM `courses`
    to_record = set(trainings) - set(records)
    indexes_to_drop = [training not in to_record for training in trainings]

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if not all(indexes_to_drop):
        # CREATES A DICT. TO SYNCHRONIZE DATABASE AND DATAFRAME COLUMNS NAME
        labels = {old: new for old, new in zip(cols, fields)}

        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'formations', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        courses.drop(index=courses.index[indexes_to_drop], inplace=True)
        courses.rename(columns=labels).to_sql(con=session.get_bind(), **kwargs)

    # RETRIEVES TRAINING ID CODES AND PUT THEM IN THE DATAFRAME
    add_trainings_id_to_dataframe(data=data, session=session)

def save_new_sessions_to_database(data, session):
    """
    Retrieves new sessions data and adds them to the 'sessions' table.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `Formation_Id`:
                See 'save_trainings_to_database' function documentation.
                Also refer to the 'add_trainings_id_to_dataframe' function.
            + `Code_Session`: Refer to `add_session_code_column_to_dataframe`.
            + `nom_departement`
            + `nom_region`
            + `code_departement`
            + `code_region`
            + `libelle_niveau_sortie_formation`
            + `intitule_certification`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        sessions to the database if there are any new sessions to add.
    """

    # BASIC SETTINGS & INITIALIZATION (Management of column names)
    keys = ['Formation_Id', 'Code_Session']            # Composite primary key
    cols = keys + ['nom_departement',                  # Dataframe column names
                   'nom_region',
                   'code_departement',
                   'code_region',
                   'libelle_niveau_sortie_formation']
    fields = keys + ['Nom_Dept',                       # Database column names
                     'Nom_Region',
                     'Code_Dept',
                     'Code_Region',
                     'Niveau_Sortie']

    # DROP ALL DUPLICATE TRAININGS FROM THE SOURCE DATAFRAME (keeps one only!)
    sort_by = keys + cols[-1:]
    courses = data[cols].sort_values(by=sort_by).drop_duplicates(subset=keys)

    # RETRIEVES THE LISTING OF THE NON DUPLICATE SESSIONS (maybe new records!) 
    modules = list(zip(*[courses[column] for column in keys]))

    # GETS ALL SESSIONS ALREADY REGISTERED IN THE DATABASE (to compare)
    records = crud.get_modules(session=session)

    # LOCATES NEW SESSIONS TO SAVE AND DEDUCES INDEXES TO DROP FROM `sessions`
    to_record = set(modules) - set(records)
    indexes_to_drop = [module not in to_record for module in modules]

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if not all(indexes_to_drop):
        # CREATES A DICT. TO SYNCHRONIZE DATABASE AND DATAFRAME COLUMNS NAME
        labels = {old: new for old, new in zip(cols, fields)}

        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'sessions', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        courses.drop(index=courses.index[indexes_to_drop], inplace=True)
        courses.rename(columns=labels).to_sql(con=session.get_bind(), **kwargs)

def update_sessions_status_in_database(data, session):
    """Not implemented yet but purpose is to update status essentially
    and alternance and Distanciel columns as well. To be considered again"""
    pass

def save_rncp_codes_to_database(data, session):
    """
    Adds RNCP codes from the dataframe that are not in the database.

    This function checks for RNCP codes in the provided dataframe and adds
    those that are not already stored in 'rncp_info' table of the database.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `code_rncp`
            + `intitule_certification`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        RNCP codes to the database if ever there are any new RNCP codes to add.
    """

    # BASIC SETTINGS & INITIALIZATION
    key = 'code_rncp'
    cols = [key, 'intitule_certification']             # Dataframe column names
    fields = ['Code', 'Libelle']                       # Database column names

    # GETS ALL CODES ALREADY REGISTERED IN THE DATABASE (to compare)
    records = crud.get_codes_list(cde_type='rncp', session=session)


    # DROP ALL DUPLICATE CODES OR NON RNCP CODES OR ALREADY REGISTERED
    codes = data[cols][data[key] != '-1'].drop_duplicates(subset=key)
    codes.drop(index=codes.index[codes[key].isin(records)], inplace=True)

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if len(codes) > 0:
        # CREATES A DICT. TO SYNCHRONIZE DATABASE AND DATAFRAME COLUMNS NAME
        labels = {old: new for old, new in zip(cols, fields)}

        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'rncp_info', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        codes.rename(columns=labels).to_sql(con=session.get_bind(), **kwargs)

def save_rs_codes_to_database(data, session):
    """
    Adds RS codes from the dataframe that are not in the database.

    This function checks for RS codes in the provided dataframe and adds
    those that are not already stored in 'rs_info' table of the database.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `code_inventaire`
            + `intitule_certification`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        RS codes to the database if ever there are any new RS codes to add.
    """

    # BASIC SETTINGS & INITIALIZATION
    key = 'code_inventaire'
    cols = [key, 'intitule_certification']             # Dataframe column names
    fields = ['Code', 'Libelle']                       # Database column names

    # GETS ALL CODES ALREADY REGISTERED IN THE DATABASE (to compare)
    records = crud.get_codes_list(cde_type='rs', session=session)

    # DROP ALL DUPLICATE CODES OR NON RNCP CODES OR ALREADY REGISTERED
    codes = data[cols][data[key] != '-1'].drop_duplicates(subset=key)
    codes.drop(index=codes.index[codes[key].isin(records)], inplace=True)

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if len(codes) > 0:
        # CREATES A DICT. TO SYNCHRONIZE DATABASE AND DATAFRAME COLUMNS NAME
        labels = {old: new for old, new in zip(cols, fields)}

        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'rs_info', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        codes.rename(columns=labels).to_sql(con=session.get_bind(), **kwargs)

def save_nsf_codes_to_database(data, session):
    """
    Adds NSF codes from the dataframe that are not in the database.

    This function checks for NSF codes in the provided dataframe and adds
    those that are not already stored in 'nsf_info' table of the database.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `nsf_code_1`
            + `nsf_code_2`
            + `nsf_code_3`
            + `libelle_nsf_1`
            + `libelle_nsf_2`
            + `libelle_nsf_3`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        NSF codes to the database if ever there are any new NSF codes to add.
    """

    # BASIC SETTINGS & INITIALIZATION
    key = 'Code'
    fields = [key, 'Libelle']                           # Database column names

    # GETS ALL CODES ALREADY REGISTERED IN THE DATABASE (to compare)
    records = crud.get_codes_list(cde_type='nsf', session=session)

    # RETRIEVES ALL NSF CODES FROM THE DATAFRAME TOGETHER WITH THEIR LABEL
    codes = []
    for i in range(1, 4):
        code, label = f'code_nsf_{i}', f'libelle_nsf_{i}'
        codes.extend(list(zip(data[code], data[label])))

    # IMPLEMENTS A DATAFRAME WITH THE RETRIEVED CODES
    codes = pd.DataFrame(columns=fields, data=codes).dropna(subset=key)

    # DROP ALL DUPLICATE CODES OR NON RNCP CODES OR ALREADY REGISTERED
    codes.drop_duplicates(subset=key, inplace=True)
    codes.drop(index=codes.index[codes[key].isin(records)], inplace=True)

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if len(codes) > 0:
        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'nsf_info', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        codes.to_sql(con=session.get_bind(), **kwargs)

def save_formacodes_to_database(data, session):
    """
    Adds formacodes from the dataframe that are not in the database.

    This function checks for formacodes in the provided dataframe and adds
    those that are not already stored in 'formacodes_info' table in database.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `code_formacode_1`
            + `code_formacode_2`
            + `code_formacode_3`
            + `code_formacode_4`
            + `code_formacode_5`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        formacodes to the database if ever there are any new formacodes to add.
    """

    # BASIC SETTINGS & INITIALIZATION
    key = 'Code'             # Primary key for target table ('formacodes_info')

    # GETS ALL CODES ALREADY REGISTERED IN THE DATABASE (to compare)
    records = crud.get_codes_list(cde_type='formacode', session=session)

    # RETRIEVES ALL NSF CODES FROM THE DATAFRAME TOGETHER WITH THEIR LABEL
    codes = []
    for i in range(1, 6):
        codes.extend(data[f'code_formacode_{i}'].dropna().tolist())

    # IMPLEMENTS A DATAFRAME WITH THE RETRIEVED CODES
    codes = pd.DataFrame(columns=[key], data=codes)

    # DROP ALL DUPLICATE CODES OR NON RNCP CODES OR ALREADY REGISTERED
    codes.drop_duplicates(subset=key, inplace=True)
    codes.drop(index=codes.index[codes[key].isin(records)], inplace=True)

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if len(codes) > 0:
        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'index': False, 'if_exists': 'append'}

        # DATA SAVING
        codes.to_sql(name='formacodes_info', con=session.get_bind(), **kwargs)

def update_codes_info_in_database(data, session):
    """Not implemented yet but purpose is to update codes title ('Libelle') and
    end date ('Date_Fin'). Target tables of the function:
    `rncp_Info`, `rs_info`, `nsf_info` and `formacodes_info`"""
    pass

def associate_trainings_and_rncp_codes(data, session):
    """
    Fills association table between trainings and RNCP codes.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `Formation_Id`:
                See 'save_trainings_to_database' function documentation.
                Also refer to the 'add_trainings_id_to_dataframe' function.
            + `code_rncp`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        association to the `rncp` table within the database if ever there are
        any new associations to add.
    """

    # BASIC SETTINGS & INITIALIZATION (Management of column names)
    cols = ['Formation_Id', 'code_rncp']  # Dataframe columns
    fields = ['Formation_Id', 'Code_RNCP']    # Database columns

    # GETS ALL CODES ALREADY REGISTERED IN THE DATABASE (to compare)
    kwargs = {'cde_type': 'rncp', 'session': session}
    records = crud.get_trainings_associations_list(**kwargs)

    # RESTRICTS DATAFRAME TO ASSOCIATIONS ONLY AND DROPS ALL DUPLICATES ROWS
    associations = data[cols][data['code_rncp'] != '-1'].dropna()
    associations = associations.drop_duplicates().sort_values('Formation_Id')

    # RETRIEVES THE LISTING OF THE NON DUPLICATE ASSOCIATIONS (maybe new ones!) 
    pairs = list(zip(*[associations[column] for column in cols]))

    # LOCATES NEW TRAININGS TO SAVE AND DEDUCES INDEXES TO DROP FROM `courses`
    to_record = set(pairs) - set(records)
    indexes_to_drop = [pair not in to_record for pair in pairs]

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if not all(indexes_to_drop):
        # CREATES A DICT. TO SYNCHRONIZE DATABASE AND DATAFRAME COLUMNS NAME
        labels = {old: new for old, new in zip(cols, fields)}

        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'rncp', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        associations.drop(index=associations.index[indexes_to_drop], inplace=True)
        associations.rename(columns=labels).to_sql(con=session.get_bind(), **kwargs)

def associate_trainings_and_formacodes(data, session):
    """
    Fills association table between trainings and formacodes.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `Formation_Id`:
                See 'save_trainings_to_database' function documentation.
                Also refer to the 'add_trainings_id_to_dataframe' function.
            + `code_formacode_1`
            + `code_formacode_2`
            + `code_formacode_3`
            + `code_formacode_4`
            + `code_formacode_5`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        association to the `formacodes` table within the database if ever there are
        any new associations to add.
    """

    # BASIC SETTINGS & INITIALIZATION (Management of column names)
    cols = ['Formation_Id'] + [f'code_formacode_{i}' for i in range(1, 6)]
    associations = data[cols].copy()     # Restrict dataset to relevant columns

    # GETS ALL CODES ALREADY REGISTERED IN THE DATABASE (to compare)
    kwargs = {'cde_type': 'formacode', 'session': session}
    records = crud.get_trainings_associations_list(**kwargs)

    # MERGES FORMACODE COLUMNS INTO NEW 'Formacode' COLUMN AND DROP ORIGINALS
    formacodes = list(zip(*[associations[col] for col in cols[1:]]))
    associations.insert(loc=1, column='Formacode', value=formacodes)
    associations.drop(columns=cols[1:], inplace=True)

    # EXPLODE 'Formacode' COLUMN INTO AS MANY ROWS AS ITEM LISTED PER CELLS
    associations['Formacode'] = associations['Formacode'].apply(list)
    associations = associations.explode(column='Formacode').dropna()

    # AS WE NOW GOT SINGLE ASSOCIATIONS WE JUST DROP DUPLICATES ONES
    associations = associations.drop_duplicates().sort_values('Formation_Id')

    # RETRIEVES THE LISTING OF ALL NON DUPLICATE ASSOCIATIONS
    # (maybe we have new ones among them! So we will compare with `records`)
    pairs = list(zip(*[associations[col] for col in associations.columns]))

    # LOCATES NEW TRAININGS TO SAVE AND DEDUCES INDEXES TO DROP FROM `courses`
    to_record = set(pairs) - set(records)
    indexes_to_drop = [pair not in to_record for pair in pairs]

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if not all(indexes_to_drop):
        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'formacodes', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        associations.drop(index=associations.index[indexes_to_drop], inplace=True)
        associations.to_sql(con=session.get_bind(), **kwargs)

def associate_trainings_and_rs_codes(data, session):
    """
    Fills association table between trainings and RS codes.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `Formation_Id`:
                See 'save_trainings_to_database' function documentation.
                Also refer to the 'add_trainings_id_to_dataframe' function.
            + `code_inventaire`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        association to the `rs` table within the database if ever there are
        any new associations to add.
    """

    # BASIC SETTINGS & INITIALIZATION (Management of column names)
    cols = ['Formation_Id', 'code_inventaire']  # Dataframe columns
    fields = ['Formation_Id', 'Code_RS']    # Database columns

    # GETS ALL CODES ALREADY REGISTERED IN THE DATABASE (to compare)
    kwargs = {'cde_type': 'rs', 'session': session}
    records = crud.get_trainings_associations_list(**kwargs)

    # RESTRICTS DATAFRAME TO ASSOCIATIONS ONLY AND DROPS ALL DUPLICATES ROWS
    associations = data[cols][data['code_inventaire'] != '-1'].dropna()
    associations = associations.drop_duplicates().sort_values('Formation_Id')

    # RETRIEVES THE LISTING OF THE NON DUPLICATE ASSOCIATIONS (maybe new ones!) 
    pairs = list(zip(*[associations[column] for column in cols]))

    # LOCATES NEW TRAININGS TO SAVE AND DEDUCES INDEXES TO DROP FROM `courses`
    to_record = set(pairs) - set(records)
    indexes_to_drop = [pair not in to_record for pair in pairs]

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if not all(indexes_to_drop):
        # CREATES A DICT. TO SYNCHRONIZE DATABASE AND DATAFRAME COLUMNS NAME
        labels = {old: new for old, new in zip(cols, fields)}

        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'rs', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        associations.drop(index=associations.index[indexes_to_drop], inplace=True)
        associations.rename(columns=labels).to_sql(con=session.get_bind(), **kwargs)

def associate_trainings_and_nsf_codes(data, session):
    """
    Fills association table between trainings and nsf codes.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame with the following columns:
            + `Formation_Id`:
                See 'save_trainings_to_database' function documentation.
                Also refer to the 'add_trainings_id_to_dataframe' function.
            + `code_nsf_1`
            + `code_nsf_2`
            + `code_nsf_3`
        session (Session): A SQLAlchemy session object for database connection. 
            For more details, refer to the SQLAlchemy documentation.

    Returns:
        None: This function does not return any value. It simply adds new
        association to the `nsf` table within the database if ever there are
        any new associations to add.
    """

    # BASIC SETTINGS & INITIALIZATION (Management of column names)
    cols = ['Formation_Id'] + [f'code_nsf_{i}' for i in range(1, 4)]
    associations = data[cols].copy()     # Restrict dataset to relevant columns

    # GETS ALL CODES ALREADY REGISTERED IN THE DATABASE (to compare)
    kwargs = {'cde_type': 'nsf', 'session': session}
    records = crud.get_trainings_associations_list(**kwargs)

    # MERGES FORMACODE COLUMNS INTO NEW 'Formacode' COLUMN AND DROP ORIGINALS
    formacodes = list(zip(*[associations[col] for col in cols[1:]]))
    associations.insert(loc=1, column='Code_NSF', value=formacodes)
    associations.drop(columns=cols[1:], inplace=True)

    # EXPLODE 'Formacode' COLUMN INTO AS MANY ROWS AS ITEM LISTED PER CELLS
    associations['Code_NSF'] = associations['Code_NSF'].apply(list)
    associations = associations.explode(column='Code_NSF').dropna()

    # AS WE NOW GOT SINGLE ASSOCIATIONS WE JUST DROP DUPLICATES ONES
    associations = associations.drop_duplicates().sort_values('Formation_Id')

    # RETRIEVES THE LISTING OF ALL NON DUPLICATE ASSOCIATIONS
    # (maybe we have new ones among them! So we will compare with `records`)
    pairs = list(zip(*[associations[col] for col in associations.columns]))

    # LOCATES NEW TRAININGS TO SAVE AND DEDUCES INDEXES TO DROP FROM `courses`
    to_record = set(pairs) - set(records)
    indexes_to_drop = [pair not in to_record for pair in pairs]

    # SAVE UNKNOWN TRAININGS INTO THE DEDICATED TABLE OF THE DATABASE
    if not all(indexes_to_drop):
        # PARAMETERS FOR SAVING PROCESS (allow short code and pep8 compliance)
        kwargs = {'name': 'nsf', 'index': False, 'if_exists': 'append'}

        # DATA SAVING
        associations.drop(index=associations.index[indexes_to_drop], inplace=True)
        associations.to_sql(con=session.get_bind(), **kwargs)

def associate_rncp_codes_and_formacodes(data, session):
    """Not implemented yet but, as indicated, purpose is to populate the
    association table between RNCP codes and Formacodes."""
    pass

def associate_rs_codes_and_formacodes(data, session):
    """Not implemented yet but, as indicated, purpose is to populate the
    association table between RS codes and Formacodes."""
    pass

def associate_rncp_and_nsf_codes(data, session):
    """Not implemented yet but, as indicated, purpose is to populate the
    association table between RNCP codes and NSF codes."""
    pass

def associate_rs_and_nsf_codes(data, session):
    """Not implemented yet but, as indicated, purpose is to populate the
    association table between RS codes and NSF codes."""
    pass

# 3. Auxiliary features (i.e. various & helper functions)
def get_dataframe(file: str = file):
    """
    Open the `.json` file and returns a dataframe. No arguments required.

    Basically, this function does a little bit more than just converting the
    source file (`.json` type). It is also a scheduler for successive cleaning
    opertaions (i.e. dedicated function calls) to finally not only return a
    dataframe but a clean dataframe. This is somehow a critical function as it
    is in charge, together with subsequent cleaning features, of ensuring the
    quality of the data finally sent to the database.

    Parameter(s):
                    By default : `TRAITEMENT_MCF/SRC/data_formation.json`
    
    Returns:
        A clean pandas dataframe.
    """

    # BASIC SETTINGS & INITIALIZATION (customizing json fields data type)
    dtype = "string[pyarrow]"
    fields = ['siret', 'code_inventaire', 'code_rncp']
    fields.extend(['code_departement', 'code_region'])
    data_dtypes = {field: dtype for field in fields}
    data_dtypes.update({f"code_nsf_{i}": dtype for i in range(1,4)})
    data_dtypes.update({f"code_formacode_{i}": dtype for i in range(1,6)})

    # LOAD THE JSON SOURCE FILE AND CHANGES IT INTO A PANDAS DATAFRAME
    data = pd.read_json(file, dtype=data_dtypes)

    # DATA CLEANING
    clean_text_columns(data)       # Remmoves extra spaces and white characters
    clean_geographic_columns(data) # Replaces `None` by '00' (in dept. codes)
    add_session_code_column_to_dataframe(data)  # Sets adhoc alphanumeric code.

    # REMOVES SIMPLON ROWS SINCE SIMPLON DATA ARE SCRAPED ELSEWHERE
    data.drop(index=data.index[data['siret'] == simplon], inplace=True)

    # REMOVES ANY ROWS HAVING NO SIRET OR NO TRAINING LABEL
    data.dropna(subset=['siret', 'intitule_formation'], inplace=True)

    # FUNCTION OUTPUT
    return data

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
              + `code_departement`
              + `libelle_niveau_sortie_formation`
              + `intitule_certification`

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

def clean_geographic_columns(data):
    """
    In-place cleaning of location codes (None values replaced by '00')

    Parameter(s):
        data: Pandas dataframe to process with following location columns.
                + `code_departement`
                + `code_region`

    Returns: Nothing, the given dataframe is modified in place.
    """

    # BASIC SETTINGS & INITIALIZATION (Set column replacement values)
    columns = {'code_departement': '00', 'code_region': '00'}

    # IN-PLACE CLEANING OF THE DATAFRAME
    data.fillna(value=columns, inplace=True)

def add_trainings_id_to_dataframe(data, session):
    """
    Retrieves trainings `Id` from the database and put them in the given frame.

    Parameter(s):
        data    : Pandas dataframe with 'siret' and 'intitule_formation'.
        session : 'session' object to connect to the database.
                  For any details see SQLAlchemy documentation.

    Returns: Nothing, the given dataframe is modified in place.
    """

    # BASIC SETTINGS é INITIALIZATION
    label = 'Formation_Id'
    columns = ['siret', 'intitule_formation']

    # GETS TRAINING ID CODES FOR TRAININGS IN THE CURRENT PANDAS DATAFRAME
    courses = list(zip(*[data[column] for column in columns]))
    trainindex = crud.get_trainings_id(session=session, trainings=set(courses))

    # INSERTS ID CODES IN THE DATAFRAME
    id_codes = [trainindex.get(course) for course in courses]
    data.insert(loc=0, column=label, value=id_codes)

def add_session_code_column_to_dataframe(data):
    """
    Retrieves trainings `Id` from the database and put them in the given frame.

    Purpose of this function is only to implement an alphanumeric code.
    This code will be part of the composite primary key defined for `sessions`
    table. But Simplon related codes are only numeric. As for the json file,
    there is not really equivalent code. The most relevant info to serve the
    same purpose is 'code_departement'. But that latter code is also numeric
    and can potentially interfere with the first one. Hence the choice to
    change it into an alphanumeric code:
    
    We simply and use unicode to convert numeric codes.
    ex: '00' is converted into 'aa00' because in unicode 'a' code is : 97 + 0

    Parameter(s):
        data    : Pandas dataframe with a `code_departement` column.

    Returns: Nothing, the given dataframe is modified in place.
    """

    # BASIC SETTINGS & INITIALIZATION
    column = 'code_departement'
    kwargs = {'loc': 0, 'column': 'Code_Session'}

    # IMPLEMENTS AN AD-HOC FUNCTION TO CONVERT NUMBERS INTO LETTERS
    convert = lambda x: ''.join(chr(97+int(i)) for i in x if i.isnumeric())

    # INSERT 'Code_Session' COLUMN INTO THE DATAFRAME () 
    data.insert(**kwargs, value=data[column].map(lambda x: f'{convert(x)}{x}'))

if __name__ == "__main__":
    # data = get_dataframe()
    # save_organizations_to_database(data)
    # save_trainings_to_database(data)
    load_data()