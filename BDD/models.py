from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import String, Date, Numeric, Boolean
from sqlalchemy import create_engine, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


# INSTANCIATING A DATABASE FRAMEWORK (i.e. a mix of container and base class) 
SimplonDB = declarative_base()

# HELPER FUNCTIONS (To simplify interactions with the 'simplon' database)
def foreign_key(target):
    """
    Returns a python list to use as arugment when calling the `column` method.

    This function helps to avoid redundancy when defining a foreign key.
    It is indeed not anymore required to explicitely indicates the data type.
    Before: `newColumn = Column(<data type>, ForeignKey(target))`
    Now   : `NewColumn = Column(*foreign_key(target))`

    Parameter(s):
        target (str): Full path to the target column
                      Ex: 'target_table_name.target_column_name'
    """

    # EXTRACTS THE TABLE AND COLUMN NAMES FROM THE 'target' ARGUMENT
    table_name, column_name = [item.strip() for item in target.split('.')]
    
    # RETRIEVES THE METADATA ABOUT THE REFERENCED COLUMN
    target_column = SimplonDB.metadata.tables[table_name].columns[column_name]
    
    # RETURNS A LIST TO BE USED AS ARGUMENT IN ANY `Column` METHOD CALL
    return [target_column.type, ForeignKey(target)]

def db_connect(url: str = "sqlite:///./simplon.db", **kwargs):
    """
    Creates or updates the database schema then returns access to it.

    The database itself is never overwritten but only udpdated or created when
    not already in place. The same for the tables inside the database.

    Parameter(s):
        url (str): url to connect the choosen database.
                   By default: "sqlite:///../simplon.db"
        **kwargs : Additional arguments to be passed to `create_engine` method.
                   For any details about the said method, see SQLAlchemy doc.
                   Example: It is possible

    Returns:
        A SQLAlchemy `sessionmaker` object to be instanciated into sessions.
    """
    # SET THE DB TYPE (sqlite, PostgreSQL, etc.) AND AN ENGINE (i.e. connector)
    engine = create_engine(url, **kwargs)

    # CREATES THE REQUIRED DATABASE (according data given into `url`)
    SimplonDB.metadata.create_all(engine)

    # FUNCTION OUTPUT (returns a `sessionmaker` object to help DB interactions)
    return sessionmaker(bind=engine)

# CREATING TABLES OF THE DATABASE
class Formations(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formations'

    # TABLE SPECIFIC COLUMNS
    # 1. Main movie characteritics
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Libelle = Column(String, nullable=False)
    code_RS = Column(String, nullable=True)
    Code_RNCP = Column(String, nullable=True)
    Niveau_Sortie = Column(String, nullable=True)
    Resume_Programme = Column(String, nullable=True)

    # 2. Tecnical details (None so far)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy model and use)
    code_nsf = relationship('CodesNSF', back_populates='formation')
    formacode = relationship('Formacodes', back_populates='formation')
    session = relationship('Sessions', back_populates='formation')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    # __table_args__ = (UniqueConstraint('Libelle',
    #                                    name='Training_name_should_be_unique'),)

class Organismes(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'organismes'

    # TABLE SPECIFIC COLUMNS
    # 1. Main movie characteritics
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nom = Column(String, nullable=False)
    Siret = Column(String, nullable=False)
    Departement = Column(*foreign_key('Departements.Id'), nullable=False)


#     # 2. Tecnical details (None so far)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy model and use)
    session =  relationship('Sessions', back_populates='location')
    code_dpt = relationship('Departements', back_populates='organisme')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (UniqueConstraint(*('Siret', 'Departement'),
                                       name='One_center_per_departement'),)

class Codes(SimplonDB): # Abstract table (for code factorization purpose)
    """
    Helps factorizing code as it is a common part of some other sub classes
    """
    # RAW PARAMETERS AND SETINGS
    __abstract__ = True

    # COLUMNS OF THE ABSTRACT TABLE
    Formation_Id = Column(*foreign_key('formations.Id'), nullable=False)
    Code = Column(String, nullable=False)
    Libelle = Column(String, nullable=True)

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Formation_Id', 'Code'),
                                           name='Composite_primary_key'),)

class Formacodes(Codes):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formacodes'

    # SPECIFIC TABLE COLUMNS
    Principal = Column(Boolean, nullable=False, default=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='formacode')

class CodesNSF(Codes):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'codes_nsf'

    # SPECIFIC TABLE COLUMNS (none at this stage !)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='code_nsf')

class Sessions(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'sessions'

    # SPECIFIC TABLE COLUMNS
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Formation_Id = Column(*foreign_key('formations.Id'), nullable=False)
    organisme_Id = Column(*foreign_key('organismes.Id'), nullable=False)
    Date_Debut = Column(Date, nullable=True)
    Type_Session  = Column(String, nullable=True)
    ville_Session  = Column(String, nullable=True)


    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='session')
    location = relationship('Organismes', back_populates='session')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (UniqueConstraint(*('Formation_Id', 'organisme_Id'),
                                       name='One_session_per_exact_location'),)

class Departements(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'departements'

    # SPECIFIC TABLE COLUMNS
    Id = Column(Integer, primary_key=True) # Ususal french dept. number
    Nom_Dept = Column(String, nullable=True)
    Nom_Region = Column(String, nullable=True)
    Code_Region = Column(Integer, nullable=True)


    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    organisme = relationship('Organismes', back_populates='code_dept')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS (None so far)
    # __table_args__ = (UniqueConstraint(*('Formation_Id', 'organisme_Id'),
    #                                    name='One_session_per_exact_location'),)