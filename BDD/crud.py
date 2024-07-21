# import dateparser, datetime
from BDD import models
from functools import wraps
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
    """

    # BASIC SETTINGS & INITIALIZATIONS
    columns = [models.Formations.Siret_OF, models.Formations.Libelle]

    # FUNCTION OUTPUT (returns a set of the query)
    return session.query(*columns).all()

# CENTRALIZED 'add' AND 'commit' FEATURES MANAGEMENT FEATURE
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