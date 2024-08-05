from functools import wraps
from sqlalchemy.orm import Session
import sqlalchemy.exc as alchemyError
import models  

# CREATING FUNCTION DECORATOR TO MANAGE SESSIONS
def manage_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) > 0:
            session = any([isinstance(argument, Session) for argument in args])
        else:
            session = isinstance(kwargs.get('session'), Session)

        if not session:
            wrapper_inner_session = models.db_connect()
            wrapper_inner_session = wrapper_inner_session()
            kwargs['session'] = wrapper_inner_session

        wrapped_function = func(*args, **kwargs)

        if not session:
            wrapper_inner_session.close()

        return wrapped_function

    return wrapper

# QUERIES SECTION
@manage_session
def get_siret(session=None):
    query = session.query(models.Organismes.Siret).all()
    return set(item[0] for item in query)

@manage_session
def get_trainings(session=None):
    columns = [models.Formations.Siret_OF, models.Formations.Libelle]
    return session.query(*columns).all()

@manage_session
def add_and_commit(items, session=None, warner="", verbose=True):
    txt = "Transaction aborted. Session rolled back"
    warner = txt if warner == "" else warner
    session.add_all(items if isinstance(items, list) else [items])

    try:
        session.commit()
    except alchemyError.IntegrityError as e:
        session.rollback()
        _ = print(warner) if warner else None
        _ = print(f'Exception details:\n{e}') if verbose else None
