import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import (
    SimplonDB, Organismes, RNCP_Info, Formacodes_Info, RS_Info, NSF_Info,
    Formations, Sessions, RNCP, Formacodes, RS, NSF, RNCP_Formacodes, RNCP_Codes_NSF,
    RS_Formacodes, RS_Codes_NSF)
from crud import manage_session
from models import Formacodes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database URL configuration
DATABASE_URL = "sqlite:///./simplon.db"

# Creating SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Creating a session local class with the database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initializing FastAPI application
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to clean session dates
def clean_session_dates(session):
    if isinstance(session.Date_Debut, str) and session.Date_Debut == '':
        session.Date_Debut = None
    if isinstance(session.Date_Lim_Cand, str) and session.Date_Lim_Cand == '':
        session.Date_Lim_Cand = None

# Endpoint to get a specific formation by its ID
@app.get("/formations/{formation_id}")
def read_formation(formation_id: int, db: Session = Depends(get_db)):
    formation = db.query(Formations).filter(Formations.Id == formation_id).first()
    if formation is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    return formation

# Endpoint to get all formations
@app.get("/formations")
def read_formations(db: Session = Depends(get_db)):
    formations = db.query(Formations).all()
    return formations

# Endpoint to get sessions by formation ID
@app.get("/sessions/{formation_id}")
def read_session_by_formation_id(formation_id: int, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Fetching sessions with Formation_Id: {formation_id}")
        sessions = db.query(Sessions).filter(Sessions.Formation_Id == formation_id).all()
        for session in sessions:
            clean_session_dates(session)
        if not sessions:
            logger.debug(f"No sessions found with Formation_Id: {formation_id}")
            raise HTTPException(status_code=404, detail="Sessions not found for the given formation ID")
        return sessions
    except Exception as e:
        logger.exception("Error fetching sessions")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get all sessions
@app.get("/sessions")
def read_sessions(db: Session = Depends(get_db)):
    try:
        logger.debug("Fetching all sessions")
        sessions = db.query(Sessions).all()
        for session in sessions:
            clean_session_dates(session)
        return sessions
    except Exception as e:
        logger.exception("Error fetching sessions")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get all organismes
@app.get("/organismes")
def read_organismes(db: Session = Depends(get_db)):
    organismes = db.query(Organismes).all()
    return organismes

# Endpoint to get a specific organisme by its SIRET
@app.get("/organismes/{siret}")
def read_organisme(siret: str, db: Session = Depends(get_db)):
    organisme = db.query(Organismes).filter(Organismes.Siret == siret).first()
    if organisme is None:
        raise HTTPException(status_code=404, detail="Organisme not found")
    return organisme

# Endpoint to get all RNCP info
@app.get("/rncp")
def read_rncps(db: Session = Depends(get_db)):
    rncps = db.query(RNCP_Info).all()
    return rncps

# Endpoint to get a specific RNCP info by its code
@app.get("/rncp/{code}")
def read_rncp(code: str, db: Session = Depends(get_db)):
    rncp_info = db.query(RNCP_Info).filter(RNCP_Info.Code == code).first()
    if rncp_info is None:
        raise HTTPException(status_code=404, detail="RNCP Info not found")
    return rncp_info

# Endpoint to get all RS info
@app.get("/rs")
def read_rss(db: Session = Depends(get_db)):
    rss = db.query(RS_Info).all()
    return rss

# Endpoint to get a specific RS info by its code
@app.get("/rs/{code}")
def read_rs(code: str, db: Session = Depends(get_db)):
    rs_info = db.query(RS_Info).filter(RS_Info.Code == code).first()
    if rs_info is None:
        raise HTTPException(status_code=404, detail="RS Info not found")
    return rs_info

# Endpoint to get all formacodes info
@app.get("/formacodes_info")
def read_formacodes(db: Session = Depends(get_db)):
    formacodes = db.query(Formacodes_Info).all()
    return formacodes

# Endpoint to get a specific formacode info by its code
@app.get("/formacodes_info/{code}")
def read_formacode(code: str, db: Session = Depends(get_db)):
    formacode_info = db.query(Formacodes_Info).filter(Formacodes_Info.Code == code).first()
    if formacode_info is None:
        raise HTTPException(status_code=404, detail="Formacode Info not found")
    return formacode_info

# Endpoint to get all formacodes info
@app.get("/formacodes")
def read_formacodes(db: Session = Depends(get_db)):
    formacodes = db.query(Formacodes).all()
    return formacodes

# Endpoint to get a specific formacode info by its code
@app.get("/formacodes/{code}")
def read_formacode(code: str, db: Session = Depends(get_db)):
    formacodes = db.query(Formacodes).filter(Formacodes.formacode == code).first()
    if formacodes is None:
        raise HTTPException(status_code=404, detail="Formacode Info not found")
    return formacodes

# Endpoint to get all NSF info
@app.get("/nsf")
def read_nsfs(db: Session = Depends(get_db)):
    nsfs = db.query(NSF_Info).all()
    return nsfs

# Endpoint to get a specific NSF info by its code
@app.get("/nsf/{code}")
def read_nsf(code: str, db: Session = Depends(get_db)):
    nsf_info = db.query(NSF_Info).filter(NSF_Info.Code == code).first()
    if nsf_info is None:
        raise HTTPException(status_code=404, detail="NSF Info not found")
    return nsf_info

# Endpoint to get all RNCP Formacodes
@app.get("/rncp_formacodes")
def read_rncp_formacodes(db: Session = Depends(get_db)):
    rncp_formacodes = db.query(RNCP_Formacodes).all()
    return rncp_formacodes

# Endpoint to get all RNCP Codes NSF
@app.get("/rncp_codes_nsf")
def read_rncp_codes_nsf(db: Session = Depends(get_db)):
    rncp_codes_nsf = db.query(RNCP_Codes_NSF).all()
    return rncp_codes_nsf

# Endpoint to get all RS Formacodes
@app.get("/rs_formacodes")
def read_rs_formacodes(db: Session = Depends(get_db)):
    rs_formacodes = db.query(RS_Formacodes).all()
    return rs_formacodes

# Endpoint to get all RS Codes NSF
@app.get("/rs_codes_nsf")
def read_rs_codes_nsf(db: Session = Depends(get_db)):
    rs_codes_nsf = db.query(RS_Codes_NSF).all()
    return rs_codes_nsf
