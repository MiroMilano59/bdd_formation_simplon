from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import String, Date, Numeric, Boolean
from sqlalchemy import create_engine, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import relationship, declared_attr, column_property


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
# Primary tables (have associations/relations but are not association tables)
class Organismes(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'organismes'

    # TABLE SPECIFIC COLUMNS
    Nom = Column(String, nullable=False)
    Siret = Column(String, primary_key=True, autoincrement=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy model and use)
    formations = relationship('Formations', back_populates='organisme')

class RNCP_Info(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp_info'

    # TABLE COLUMNS
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=False)
    Date_Fin = Column(Date, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('RNCP', back_populates='code_rncp')
    formacodes = relationship('RNCP_Formacodes', back_populates='code_rncp')
    codes_nsf = relationship('RNCP_Codes_NSF', back_populates='code_rncp')

class Formacodes_Info(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formacodes_info'

    # TABLE COLUMNS
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('Formacodes', back_populates='formacode')
    codes_rncp = relationship('RNCP_Formacodes', back_populates='formacode')
    codes_rs = relationship('RS_Formacodes', back_populates='formacode')

class RS_Info(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rs_info'

    # TABLE COLUMNS
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=False)
    Date_Fin = Column(Date, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('RS', back_populates='code_rs')
    formacodes = relationship('RS_Formacodes', back_populates='code_rs')
    codes_nsf = relationship('RS_Codes_NSF', back_populates='code_rs')

class NSF_Info(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'nsf_info'

    # TABLE COLUMNS
    Code = Column(String, primary_key=True, autoincrement=False)
    Libelle = Column(String, nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formations = relationship('NSF', back_populates='code_nsf')
    codes_rncp = relationship('RNCP_Codes_NSF', back_populates='code_nsf')
    codes_rs = relationship('RS_Codes_NSF', back_populates='code_nsf')

# Core association tables
class Formations(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formations'

    # TABLE SPECIFIC COLUMNS
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Libelle = Column(String, nullable=False)
    Siret_OF = Column(*foreign_key('organismes.Siret'), nullable=False)
    Niveau_Sortie = Column(String, nullable=True)
    Resume_Programme = Column(String, nullable=True)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy model and use)
    codes_rs = relationship('RS', back_populates='formation')
    sessions = relationship('Sessions', back_populates='formation')
    codes_nsf = relationship('NSF', back_populates='formation')
    organisme = relationship('Organismes', back_populates='formations')
    formacodes = relationship('Formacodes', back_populates='formation')
    codes_rncp = relationship('RNCP', back_populates='formation')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (UniqueConstraint(*('Libelle', 'Siret_OF'),
                                       name='Libelle+Siret_OF_is_unique!'),)

class Sessions(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'sessions'

    # SPECIFIC TABLE COLUMNS
    Formation_Id = Column(*foreign_key('formations.Id'), nullable=False)
    Nom_Dept = Column(String, nullable=True)
    Code_Dept = Column(Integer, nullable=False) # Ususal french dept. number
    Nom_Region = Column(String, nullable=True)
    Code_Region = Column(Integer, nullable=True)
    Ville = Column(String, nullable=True)
    Date_Debut = Column(Date, nullable=True)
    Date_Lim_Cand = Column(Date, nullable=True)
    Duree = Column(String, nullable=True)
    Alternance = Column(Boolean, nullable=True, default=False)
    Distanciel = Column(Boolean, nullable=True, default=False)
    Libelle_certif = Column(String, nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='sessions')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Formation_Id', 'Code_Dept'),
                                           name='Composite_primary_key'),)

# Secondary association tables
class RNCP(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp'

    # TABLE COLUMNS
    Formation_Id = Column(*foreign_key('formation.Id'), nullable=False)
    Code_RNCP = Column(*foreign_key('rncp_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='codes_rncp')
    code_rncp = relationship('RNCP_Info', back_populates='formations')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Formation_Id', 'Code_RNCP'),
                                           name='Composite_primary_key'),)

class Formacodes(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'formacodes'

    # TABLE COLUMNS
    Formation_Id = Column(*foreign_key('formation.Id'), nullable=False)
    Formacode = Column(*foreign_key('formacodes_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='formacodes')
    formacode = relationship('Formacodes_Info', back_populates='formations')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Formation_Id', 'Formacode'),
                                           name='Composite_primary_key'),)

class RS(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rs'

    # TABLE COLUMNS
    Formation_Id = Column(*foreign_key('formation.Id'), nullable=False)
    Code_RS = Column(*foreign_key('rs_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='codes_rs')
    code_rs = relationship('RS_Info', back_populates='formations')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Formation_Id', 'Code_RS'),
                                           name='Composite_primary_key'),)

class NSF(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rs'

    # TABLE COLUMNS
    Formation_Id = Column(*foreign_key('formation.Id'), nullable=False)
    Code_NSF = Column(*foreign_key('nsf_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    formation = relationship('Formations', back_populates='codes_nsf')
    code_nsf = relationship('NSF_Info', back_populates='formations')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Formation_Id', 'Code_NSF'),
                                           name='Composite_primary_key'),)

# Auxiliary association tables
class RNCP_Formacodes(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp_formacodes'

    # TABLE COLUMNS
    Code_RNCP = Column(*foreign_key('rncp_info.code'), nullable=False)
    formacode = Column(*foreign_key('formacode_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    code_rncp = relationship('RNCP_Info', back_populates='formacodes')
    formacode = relationship('Formacodes_Info', back_populates='codes_rncp')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Code_RNCP', 'formacode'),
                                           name='Composite_primary_key'),)

class RNCP_Codes_NSF(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp_code_nsf'

    # TABLE COLUMNS
    Code_RNCP = Column(*foreign_key('rncp_info.Code'), nullable=False)
    Code_NSF = Column(*foreign_key('nsf_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    code_nsf = relationship('NSF_Info', back_populates='codes_rncp')
    code_rncp = relationship('RNCP_Info', back_populates='codes_nsf')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Code_RNCP', 'Code_NSF'),
                                           name='Composite_primary_key'),)

class RS_Formacodes(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp_code_nsf'

    # TABLE COLUMNS
    Code_RS = Column(*foreign_key('rs_info.Code'), nullable=False)
    Formacode = Column(*foreign_key('formacodes_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    code_rs = relationship('RS_Info', back_populates='formacodes')
    formacode = relationship('Formacodes_Info', back_populates='codes_rs')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Code_RS', 'Formacode'),
                                           name='Composite_primary_key'),)

class RS_Codes_NSF(SimplonDB):
    # RAW PARAMETERS AND SETINGS
    __tablename__ = 'rncp_code_nsf'

    # TABLE COLUMNS
    Code_RS = Column(*foreign_key('rs_info.Code'), nullable=False)
    Code_NSF = Column(*foreign_key('nsf_info.Code'), nullable=False)

    # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
    code_rs = relationship('RS_Info', back_populates='codes_nsf')
    code_nsf = relationship('NFS_Info', back_populates='codes_rs')

    # DEFINING SCHEMA SPECIFIC CONSTRAINTS
    __table_args__ = (PrimaryKeyConstraint(*('Code_RS', 'Code_NSF'),
                                           name='Composite_primary_key'),)













# class Codes_Info(SimplonDB): # Abstract table (code factorization purpose)
#     """
#     Helps factorizing code as it is a common part of some other sub classes

#     Main purpose is to give an almost ready to use table for all code tables.
#     """
#     # RAW PARAMETERS AND SETINGS
#     __abstract__ = True

#     # COLUMNS OF THE ABSTRACT TABLE
#     Code = Column(String, primary_key=True, autoincrement=False)
#     Libelle = Column(String, nullable=False)

# class RCNP_Info(Codes_Info):
#     # RAW PARAMETERS AND SETINGS
#     __tablename__ = 'rncp_info'

#     # SPECIFIC COLUMNS OF THE TABLE
#     Date_fin = Column(Date, nullable=True)

#     # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
#     formations = relationship('RNCP', back_populates='codes_rncp')
#     # formacodes = relationship('RNCP-Formacodes', back_populates='codes_rncp')
#     # nsf_codes = relationship('RNCP-NSF_Codes', back_populates='codes_rncp')

# class Formacodes_Info(Codes_Info):
#     # RAW PARAMETERS AND SETINGS
#     __tablename__ = 'rncp_info'

#     # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
#     formations = relationship('Formacodes', back_populates='formacodes')
#     # rncp_codes = relationship('RNCP-Formacodes', back_populates='codes_rncp')
#     # rs_codes

# class Codes_Associations(SimplonDB): # Abstract table (factorization purpose)
#     """
#     Helps factorizing code as it is a common part of some other sub classes

#     Purpose is to give a ready to use table for all codes association tables.
#     """
#     # RAW PARAMETERS AND SETINGS
#     __abstract__ = True

#     # COLUMNS OF THE ABSTRACT TABLE
#     @declared_attr
#     def column1(cls):
#         column = Column(*foreign_key('RNCP_Info.Code'),
#                                       name='Code_Rncp',
#                                       nullable=False))
#         return column_property(column)

# # Column(*foreign_key('RNCP_Info.Code'),
# #                                       name='Code_Rncp',
# #                                       nullable=False))

#     # Code = Column(String, primary_key=True, autoincrement=False)
#     # Libelle = Column(String, nullable=False)

# class RCNP(SimplonDB):
#     # RAW PARAMETERS AND SETINGS
#     __tablename__ = 'rncp'

#     # COLUMNS OF THE ABSTRACT TABLE
#     Code_Rncp = Column(*foreign_key('RNCP_Info.Code'), nullable=False)
#     Formation_Id = Column(*foreign_key('formations.Id'), nullable=False)

#     # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
#     formations = relationship('Formations', back_populates='codes_rncp')
#     codes_rncp = relationship('RNCP_Info', back_populates='formations')

#     # DEFINING SCHEMA SPECIFIC CONSTRAINTS
#     __table_args__ = (PrimaryKeyConstraint(*('Code_Rncp', 'Formation_Id'),
#                                            name='Composite_primary_key'),)

# class Formacodes(Codes):
#     # RAW PARAMETERS AND SETINGS
#     __tablename__ = 'formacodes'

#     # SPECIFIC TABLE COLUMNS
#     Principal = Column(Boolean, nullable=False, default=False)

#     # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
#     formation = relationship('Formations', back_populates='formacode')

# class CodesNSF(Codes):
#     # RAW PARAMETERS AND SETINGS
#     __tablename__ = 'codes_nsf'

#     # SPECIFIC TABLE COLUMNS (none at this stage !)

#     # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
#     formation = relationship('Formations', back_populates='code_nsf')

# class Departements(SimplonDB):
#     # RAW PARAMETERS AND SETINGS
#     __tablename__ = 'departements'

#     # SPECIFIC TABLE COLUMNS



#     # DEFINING PURE ORM RELATIONSHIPS (i.e. enhancing SQLAlchemy features)
#     organisme = relationship('Organismes', back_populates='code_dept')

#     # DEFINING SCHEMA SPECIFIC CONSTRAINTS (None so far)
#     # __table_args__ = (UniqueConstraint(*('Formation_Id', 'organisme_Id'),
#     #                                    name='One_session_per_exact_location'),)

# class Codes(SimplonDB): # Abstract table (for code factorization purpose)
#     """
#     Helps factorizing code as it is a common part of some other sub classes

#     Main purpose is to give an almost ready to use table for all code tables.
#     """
#     # RAW PARAMETERS AND SETINGS
#     __abstract__ = True

#     # COLUMNS OF THE ABSTRACT TABLE
#     Formation_Id = Column(*foreign_key('formations.Id'), nullable=False)
#     Code = Column(String, nullable=False)
#     Libelle = Column(String, nullable=True)

#     # DEFINING SCHEMA SPECIFIC CONSTRAINTS
#     __table_args__ = (PrimaryKeyConstraint(*('Formation_Id', 'Code'),
#                                            name='Composite_primary_key'),)