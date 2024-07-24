# import dateparser, datetime
from BDD import models
from functools import wraps
from sqlalchemy import or_
from sqlalchemy.orm import Session
import sqlalchemy.exc as alchemyError

# CREATING FUNCTION DECORATOR TO MANAGE SESSIONS
def manage_session(func):
    """
    FUNCTION DECORATOR : Gives functions a session and close it at the end.

    The purpose of this decorator is to check whether the decorated functions
    have been given a Session on call. Otherwise, it gives them one and closes
    it after the function executes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # BASIC SETTINGS AND INITIALIZATION (looking whether a session exists)
        if len(args) > 0:
            session = any([isinstance(argument, Session) for argument in args])
        else:
            session = isinstance(kwargs.get('session'), Session)

        # CREATES A TEMPORARY SESSION IF NON WAS PROVIDED ON FUNCTION CALL
        if not session:
            wrapper_inner_session = models.db_connect()
            wrapper_inner_session = wrapper_inner_session()
            kwargs['session'] = wrapper_inner_session

        # EXECUTION OF THE FUNCTION
        wrapped_function = func(*args, **kwargs)

        # CLOSING TEMPORARY SESSION
        if not session:
            wrapper_inner_session.close()

        # WRAPPER OUTPUT
        return wrapped_function

    # DECORATOR OUTPUT
    return wrapper

# QUERIES SECTION
@manage_session
def get_siret(session=None):
    """
    Returns a set of all siret already in the 'organinsme' table of the DB.

    Parameter(s):
        session : OPTIONAL. SQLAlchemy session object. If not provided then one
                  temporary session will be open and closed at the end.
    """
    # QUERYING THE DATABASE
    query = session.query(models.Organismes.Siret).all()

    # FUNCTION OUTPUT (Explodes tuples in the result and returns a set)
    return set(item[0] for item in query)

@manage_session
def get_trainings(session=None):
    """
    Returns a set of all trainings already in the 'formations' table of the DB.

    Parameter(s):
        session : OPTIONAL. SQLAlchemy session object. If not provided then one
                  temporary session will be open and closed at the end.
    
    Returns: A python list of tuples formated like ("siret", "libelle")
    """

    # BASIC SETTINGS & INITIALIZATIONS
    columns = [models.Formations.Siret_OF, models.Formations.Libelle]

    # FUNCTION OUTPUT (returns a set of the query)
    return session.query(*columns).all()

@manage_session
def get_modules(session=None):
    """
    Returns a set of all sessions (or modules) already in the 'sessions' table.

    Parameter(s):
        session : OPTIONAL. SQLAlchemy session object. If not provided then one
                  temporary session will be open and closed at the end.
    
    Returns:
        A python list of tuples formated like ("Formation_Id", "Code_Session")
    """

    # BASIC SETTINGS & INITIALIZATIONS
    columns = [models.Sessions.Formation_Id, models.Sessions.Code_Session]

    # FUNCTION OUTPUT (returns a set of the query)
    return session.query(*columns).all()

@manage_session
def get_codes_list(cde_type, session=None):
    """
    Returns a list with all the specified code type already registered

    Parameters:
        cde_type (str): The type of the code between:
            + `rs`
            + `nsf`
            + `rncp`
            + `formacode` : Default value
        session (optional): SQLAlchemy session object. If not provided, then
            a temporary session will be opened and closed at the end.

    Returns: python list
    """

    # BASIC SETTINGS & INITIALIZATIONS (implements a table selector)
    table = {'rs': models.RS_Info,
              'nsf': models.NSF_Info,
              'rncp': models.RNCP_Info,
              'formacode': models.Formacodes_Info}

    # PROCESSING USER CHOICE FOR `type` PARAMETER
    cde_type = cde_type.lower() if isinstance(cde_type, str) else 'formacode'
    cde_type = cde_type if cde_type in table.keys() else 'formacode'


    # FUNCTION OUTPUT (returns a set of the query)
    return set(item[0] for item in session.query(table[cde_type].Code).all())

@manage_session
def get_trainings_id(trainings=None, session=None, as_dict=True):
    """
    Returns the unique `Id` code for each of the specified trainings.
 
    Parameter(s):
        trainings (tuple | list, optional):
            - If `None` (default), returns all known training `Id` codes.
            - If a tuple like (`Siret_OF`, `Libelle`), returns the `Id` code
              for that specific training.
            - If a list of tuples, returns `Id` codes for these trainings.
        session (session, optional): SQLAlchemy session object.
            If not provided, a temporary session will be created and closed
            automatically once query is complete.
        as_dict (bool): Whether to get the result as a dictionary (default)
                        or to get it as a simple list of tuples like:
                        (`Siret_OF`, `Libelle`, `Id`)

    Returns:
        dict | list: Either a dictionary (default) where keys are the specified
            training tuples and the values are the related `Id` codes. Or a
            list of tuples (for details see `Parameter(s)` section)
    """

    # BASIC SETTINGS & INITIALIZATIONS
    table = models.Formations                                  # Target table
    #filters = True  # Default filter old version. Wait for days before delete!
    filters = [True]                                           # Default filter
    columns = ['Siret_OF', 'Libelle', 'Id']                    # Target columns
    columns = [getattr(table, column) for column in columns]   # Target columns

    # IMPLEMENTS USER-SPECIFIED FILTERS TO USE INSTEAD OF ABOVE DEFAULT FILTER
    if not trainings is None:
        # MANAGE THE USER'S CHOICE RELATING TO THE 'trainings' PARAMETER
        #filters = [trainings] if isinstance(trainings, tuple) else trainings
        fltrs = [trainings] if isinstance(trainings, tuple) else trainings

        # IMPLEMENTS USER-SPECIFIED FILTERS
        # OLD # filters = or_(*[(columns[0] == siret) & (columns[1] == libelle)
        # OLD #                 for siret, libelle in filters])
        fltrs = [(columns[0] == siret) & (columns[1] == libelle)
                        for siret, libelle in fltrs]

        # NEXT STAGE (chunking request to process it by batch)
        batch = 500   # Batch size (sqlite cannot treat more than 1000 at once)
        filters = [or_(*fltrs[i:i+batch]) for i in range(0, len(fltrs), batch)]

    # EXECUTES QUERY
    # OLD #query = session.query(*columns).filter(filters).all()
    query = []
    for conditions in filters:
        query.extend(session.query(*columns).filter(conditions).all())

    # FUNCTION OUTPUT (returns a set of the query)
    if as_dict:
        return {training[:-1]: training[-1] for training in query}
    else:
        return query

# CENTRALIZED FEATURE FOR 'add' AND 'commit' DATABASE FEATURES MANAGEMENT
@manage_session
def add_and_commit(items, session=None, warner="", verbose=True):
    """
    Commit changes if ACID compliant or rollback otherwise with message.

    Parameter(s):
        item    (list): Instance(s) to be added to their respective tables.
                        `item` can be either a single instance or a list of
                        instances to add to the database.
        session       : OPTIONAL. SQLAlchemy sesson object. If not provided
                        then one temporary session will be open and closed
                        at the end.
        warner   (str): OPTIONAL. Message to display if transaction aborted.
                        Default: `Transaction aborted. Session rolled back`
                        Optionally : `warner` can be set to None in order not
                        to show any warning message. At your own risk !
        verbose (bool): Whether to gives details when exceptions raised.
                        Default value is True.
    """
    # PROCESSING WARNING MESSAGE
    txt = "Transaction aborted. Session rolled back"
    warner = txt if warner == "" else warner

    # ADDING GIVEN INSTANCE TO THE DATABASE
    #session.add(item)                    # Old release/version of the function
    session.add_all(items if isinstance(items, list) else [items])

    # COMMITING PROCESS (validation of the transaction of restoring last state)
    try:
        session.commit()
    except alchemyError.IntegrityError as e:
        session.rollback()
        _ = print(warner) if warner else None
        _ = print(f'Exception details:\n{e}') if verbose else None


#print(type(get_siret()))


# VARIOUS FROM OTHER SIMILAR PROJECTS (inspiration purpose)
# @manage_session
# def get_movie_id(title, date=None, session=None, warns=True):
#     """
#     Check the database and returns the `Id` of a movie (`MovieId`)

#     Parameter(s)
#         title                (str): French title of the target movie.
#         date   (str|datetime.date): Release date of the target movie.
#         session          (Session): OPTIONAL. SQLAlchemy session to use. If one
#                                     session is provided, then it is simply used
#                                     but not closed. if no session is provided,
#                                     then one is open and closed at the end.
#     """

#     # BASIC SETTINGS & INITIALIZATION (try to parse date if given as a string)
#     if not isinstance(date, datetime.date):
#         date = dateparser.parse(date) if date else None
#         date = date.date() if date else None

#     # WARNS USER WHEN DATE IS `BAD` (i.e. when `date` still is None)
#     if warns and not isinstance(date, datetime.date):
#         print("WARNING: bad date. Please check it and retry if no result.")

#     # QUERYING THE DATABASE
#     query = (session
#              .query(schema.Movies.Id)
#              .filter_by(Title_Fr=title, Release_Date=date)
#              .first())

#     # FUNCTION OUTPUT
#     return query[0]

# @manage_session
# def get_persons_id(names, session=None):
#     """
#     Returns a dictionary with required names as keys and `Id` as values.

#     Parameter(s)
#         names (str|tuple|list|set): Names of people whose `Id` is requested.
#                                     Either a single string or a collection of
#                                     strings.
#         session          (Session): OPTIONAL. SQLAlchemy session to use. If one
#                                     session is provided, then it is simply used
#                                     but not closed. if no session is provided,
#                                     then one is open and closed at the end.
#     """

#     # BASIC SETTINGS & INITIALIZATION
#     names = [names] if isinstance(names, str) else names

#     # QUERYING THE DATABASE
#     query = (session
#              .query(schema.Persons.Id, schema.Persons.Full_Name)
#              .filter(schema.Persons.Full_Name.in_(names))
#              .all())

#     # FUNCTION OUTPUT
#     return {full_name: code_id for code_id, full_name in query}

# @manage_session
# def get_companies_id(names, session=None):
#     """
#     Returns a dictionary with company names as keys and `Id` as values.

#     Parameter(s)
#         names (str|tuple|list|set): Names of people whose `Id` is requested.
#                                     Either a single string or a collection of
#                                     strings.
#         session          (Session): OPTIONAL. SQLAlchemy session to use. If one
#                                     session is provided, then it is simply used
#                                     but not closed. if no session is provided,
#                                     then one is open and closed at the end.
#     """

#     # BASIC SETTINGS & INITIALIZATION
#     names = [names] if isinstance(names, str) else names

#     # QUERYING THE DATABASE
#     query = (session
#              .query(schema.Companies.Id, schema.Companies.Full_Name)
#              .filter(schema.Companies.Full_Name.in_(names))
#              .all())

#     # FUNCTION OUTPUT
#     return {full_name: code_id for code_id, full_name in query}

# # QUERIES TESTING
# # print(get_persons_id(['Alexandre De La Patellière',
# #                       'Pierfrancesco Favino',
# #                       'Adèle Simphal']))

# #print(get_persons_id(set('gaston')))

# #print(get_movie_id(title='The Bikeriders', date='2024/06/19'))

# #print(get_companies_id(["Bac Films", "toto et les moutons démoniaques"]))