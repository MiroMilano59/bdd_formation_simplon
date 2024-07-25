#import schema # For test purpose only (and obly this python script !)
# import dateparser, datetime
from functools import wraps
from sqlalchemy.orm import Session
import sqlalchemy.exc as alchemyError
import models


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

# Methods to integrate RNCP_Info
@manage_session
def get_rncp_code(rncpcode, session=None, warns=True):
    """
    Check the database rncp_info table if RNCP Code

    Parameter(s)
        rncpcode            (int):  RNCP Code.
        item                (int): item to insert in rncp_info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # QUERYING THE DATABASE
    query = (session
             .query(models.RNCP_Info)
             .filter_by(Code=rncpcode)
             .first())
    
    value_to_return = False

    if query:
        value_to_return = True

    # FUNCTION OUTPUT query[0]
    return value_to_return

@manage_session
def insert_rncp_code(rncpcode, libelle, date_fin, session=None, warns=True):
    """
    Insert new RNCP code infos into rncp_info table

    Parameter(s)
        rncpcode            (int): RNCP code.
        item                (int): item to insert in rncp_info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    rncp = models.RNCP_Info(Code=rncpcode,Libelle=libelle,Date_Fin=date_fin)
    session.add(rncp)
    session.commit()
    session.close()

# Methods to integrate Formacodes_Info
@manage_session
def get_formacode(formacode, session=None, warns=True):
    """
    Check the database Formacodes_Info table if Formacode Exists

    Parameter(s)
        formacode           (int):  Formacode.
        item                (int): item to insert in Formacodes_Info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # QUERYING THE DATABASE
    query = (session
             .query(models.Formacodes_Info)
             .filter_by(Code=formacode)
             .first())
    
    value_to_return = False

    if query:
        value_to_return = True

    # FUNCTION OUTPUT query[0]
    return value_to_return

@manage_session
def insert_formacode(formacode, libelle, session=None, warns=True):
    """
    Insert new formacode infos into formacodes_info table

    Parameter(s)
        formacode           (int): formacode.
        item                (int): item to insert into  formacodes_info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    formacodeinfo = models.Formacodes_Info(Code=formacode,Libelle=libelle)
    session.add(formacodeinfo)
    session.commit()
    session.close()
# Insert formacode id formation on formacodes table
@manage_session
def insert_formacode_table(formacode, idformation, session=None, warns=True):
    """
    Insert new formacode infos into formacodes_info table

    Parameter(s)
        formacode           (int): formacode.
        item                (int): item to insert into  formacodes_info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    formacodeinfo = models.Formacodes(Formation_Id=idformation, Formacode=formacode)
    session.add(formacodeinfo)
    session.commit()
    session.close()

# Insert nsf code id formation on nsf table
@manage_session
def insert_nsf_table(nsfcode, idformation, session=None, warns=True):
    """
    Insert new nsf infos into nsf table

    Parameter(s)
        nsfcode             (int): nsf code.
        item                (int): item to insert into  nsf table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    nsf = models.NSF(Formation_Id=idformation, Code_NSF=nsfcode)
    session.add(nsf)
    session.commit()
    session.close()

@manage_session
def insert_rs_table(rscode, idformation, session=None, warns=True):
    """
    Insert new rs code into rs table

    Parameter(s)
        rscode              (int): RS Code.
        item                (int): item to insert into  rs table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    rs = models.RS(Formation_Id=idformation, Code_RS=rscode)
    session.add(rs)
    session.commit()
    session.close()

@manage_session
def insert_rncp_table(rncpcode, idformation, session=None, warns=True):
    """
    Insert RNCP Code infos into rncp table

    Parameter(s)
        rncpcode            (int): RNCP Code.
        item                (int): item to insert into  rncp table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    rncp = models.RNCP(Formation_Id=idformation, Code_RNCP=rncpcode)
    session.add(rncp)
    session.commit()
    session.close()

@manage_session
def insert_rncp_nsf_table(rncpcode, nsfcode, session=None, warns=True):
    """
    Insert new rncp into rncp nsf into rncp_codes_nsf association table

    Parameter(s)
        rncpcode            (int): rncp.
        item                (int): item to insert into  rncp_codes_nsf association table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    rncp_nfs = models.RNCP_Codes_NSF(Code_RNCP=rncpcode, Code_NSF=nsfcode)
    session.add(rncp_nfs)
    session.commit()
    session.close()

@manage_session
def insert_rs_nsf_table(rscode, nsfcode, session=None, warns=True):
    """
    Insert new rs nsf code infos into rs_codes_nsf association table

    Parameter(s)
        rscode              (int): RS Code.
        item                (int): item to insert into  rs_codes_nsf association table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    rs_nfs = models.RS_Codes_NSF(Code_RS=rscode, Code_NSF=nsfcode)
    session.add(rs_nfs)
    session.commit()
    session.close()

@manage_session
def insert_rncp_formacode_table(rncpcode, formacode, session=None, warns=True):
    """
    Insert new rncp formacodes infos into rncp formacodes association table

    Parameter(s)
        rncpcode            (int): RNCP Code.
        item                (int): item to insert into  rncp_formacodes association table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    rncp_formacode = models.RNCP_Formacodes(Code_RNCP=rncpcode, Formacode=formacode)
    session.add(rncp_formacode)
    session.commit()
    session.close()

@manage_session
def insert_rs_formacode_table(rscode, formacode, session=None, warns=True):
    """
    Insert new rs formacodes infos into rs_formacodes association table

    Parameter(s)
        rscode              (int): RS Code.
        item                (int): item to insert into  rs_formacodes association table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RNCP INTO TABLE
    rs_formacode = models.RS_Formacodes(Code_RS=rscode, Formacode=formacode)
    session.add(rs_formacode)
    session.commit()
    session.close()

# Methods to integrate RS_Info
@manage_session
def get_rs_code(rscode, session=None, warns=True):
    """
    Check the database rs_info table if Rs Code exists

    Parameter(s)
        rscode              (int):  RS Code.
        item                (int): item to insert in rs_info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # QUERYING THE DATABASE
    query = (session
             .query(models.RS_Info)
             .filter_by(Code=rscode)
             .first())
    
    value_to_return = False

    if query:
        value_to_return = True

    # FUNCTION OUTPUT query[0]
    return value_to_return

@manage_session
def insert_rs_code(rscode, libelle, date_fin, session=None, warns=True):
    """
    Insert new RS code infos into rs_info table

    Parameter(s)
        rscode              (int): RS Code.
        item                (int): item to insert in into rs_info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RS INTO TABLE
    rs = models.RS_Info(Code=rscode,Libelle=libelle,Date_Fin=date_fin)
    session.add(rs)
    session.commit()
    session.close()

# Methods to integrate NSF_Info
@manage_session
def get_nsf_code(nsfcode, session=None, warns=True):
    """
    Check the database nsf_info table if NSF Code exists

    Parameter(s)
        code                (int):  NSF Code.
        item                (int): item to insert in rs_info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # QUERYING THE DATABASE
    query = (session
             .query(models.NSF_Info)
             .filter_by(Code=nsfcode)
             .first())
    
    value_to_return = False

    if query:
        value_to_return = True

    # FUNCTION OUTPUT query[0]
    return value_to_return

@manage_session
def insert_nsf_code(nsfcode, libelle, session=None, warns=True):
    """
    Insert new NSF code infos into nsf_info table

    Parameter(s)
        code                (int): NSF Code.
        item                (int): item to insert in into nsf_info table.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # INSERT RS INTO TABLE
    nsf = models.NSF_Info(Code=nsfcode,Libelle=libelle)
    session.add(nsf)
    session.commit()
    session.close()

# Methods to integrate Formations Infos
@manage_session
def get_formation(idsimplon, session=None, warns=True):
    """
    Check the database formations table if formation exists

    Parameter(s)
        idsimplon           (int):  id simplon scrpaed from simplon site web.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # QUERYING THE DATABASE
    query = (session
             .query(models.Formations)
             .filter_by(Simplon_Id=idsimplon)
             .first())
    
    value_to_return = False

    if query:
        value_to_return = True

    # FUNCTION OUTPUT query[0]
    return value_to_return

@manage_session
def get_id_formation(idsession, session=None, warns=True):
    """
    Check the database formations table if formation exists and get formation Id

    Parameter(s)
        idsession           (int):  id simplon scrpaed from simplon site web of session.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

    # QUERYING THE DATABASE
    query = (session
             .query(models.Formations.Id)
             .filter_by(Simplon_Id=idsession)
             .first())
    
    return query[0]


@manage_session
def insert_formation(idsimplon, libelle, resumeprogramme, session=None, warns=True, siretsimplon="79279132900032"):
    """
    Insert new formation infos into formations table

    Parameter(s)
        idsimplon           (int): id simplon scrpaed from simplon site web.
        libelle             (str): formation name scraped from simplon site web.
        resumeprogramme     (str): formation summary programm.
        siretsimplon        (str): simplon SIRET unique code.
        session         (Session): OPTIONAL. SQLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.
    """

     # INSERT NEW FORMATIOIN  INTO  formations TABLE
    formation = models.Formations(Simplon_Id=idsimplon,
                                  Libelle=libelle,
                                  Siret_OF=siretsimplon,
                                  Resume_Programme=resumeprogramme
                                  )
    session.add(formation)
    session.commit()
    session.close()


@manage_session
def insert_organisme_test(session=None, warns=True):

    """Insert new organisme, Simplon with SIRET 79279132900032
    """

    organisme = models.Organismes(Nom="Simplon",
                                  Siret="79279132900032")
    session.add(organisme)
    session.commit()
    # session.close()


@manage_session
def insert_session(formationid, 
                   codesession, 
                   niveausortie,
                   nomdept,
                   codedept,
                   datedebut,
                   datelimitcand,
                   duree,
                   libellecertif,
                   alternance,
                   distance,
                   session=None, 
                   warns=True
                   ):
    """_summary_

    Args:
        formationid (int): id formation from formations table
        codesession (str): code session scraped from simplon web site
        nomdept (str): nom departement
        codedept (int): code departement
        datedebut (date): date start session
        datelimitcand (date): application deadline 
        duree (str): duration
        alternance (bool): alternance
        distanciel (bool): distanciel
        niveausortie (str): niveau de sortie
        libellecertif (str): libelle certification
        session (_type_, optional): QLAlchemy session to use. If one
                                    session is provided, then it is simply used
                                    but not closed. if no session is provided,
                                    then one is open and closed at the end.. Defaults to "79279132900032".. Defaults to None.
        warns (bool, optional): _description_. Defaults to True.
    """
     # INSERT NEW FORMATIOIN  INTO  formations TABLE
    session_to_insert = models.Sessions(Formation_Id=formationid,
                              Code_Session=codesession,
                              Nom_Dept=nomdept,
                              Code_Dept=codedept,
                              Date_Debut=datedebut,
                              Date_Lim_Cand=datelimitcand,
                              Duree=duree,
                              Alternance=alternance,
                              Distanciel=distance,
                              Niveau_Sortie=niveausortie,
                              Libelle_Session=libellecertif
                              )
    session.add(session_to_insert)
    session.commit()
    session.close()
