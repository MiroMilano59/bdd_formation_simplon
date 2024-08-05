# from sqlalchemy import create_engine, inspect
# from sqlalchemy.orm import sessionmaker
# from models import SimplonDB, Sessions, Formations, Organismes, RNCP_Info, Formacodes_Info, RS_Info, NSF_Info

# DATABASE_URL = "sqlite:///./simplon.db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
# db = SessionLocal()

# # Créer les tables si elles n'existent pas
# SimplonDB.metadata.create_all(engine)

# # Vérifiez que la table sessions existe
# inspector = inspect(engine)
# if not inspector.has_table("sessions"):
#     print("La table 'sessions' n'existe pas")
# else:
#     print("La table 'sessions' existe")

# # Vous pouvez également vérifier les autres tables de la même manière
# if not inspector.has_table("formations"):
#     print("La table 'formations' n'existe pas")
# else:
#     print("La table 'formations' existe")

# # Nettoyage des données
# sessions = db.query(Sessions).all()
# for session in sessions:
#     if session.Date_Debut == '':
#         session.Date_Debut = None
#     if session.Date_Lim_Cand == '':
#         session.Date_Lim_Cand = None
# db.commit()
# print("Nettoyage terminé")



# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Sessions

# DATABASE_URL = "sqlite:///./simplon.db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
# db = SessionLocal()

# # Nettoyage des données
# sessions = db.query(Sessions).all()
# for session in sessions:
#     if session.Date_Debut == '':
#         print(f"Correction de Date_Debut pour la session {session.Formation_Id}")
#         session.Date_Debut = None
#     if session.Date_Lim_Cand == '':
#         print(f"Correction de Date_Lim_Cand pour la session {session.Formation_Id}")
#         session.Date_Lim_Cand = None
# db.commit()
# print("Nettoyage terminé")

# # Vérifiez que les données ont été nettoyées
# sessions = db.query(Sessions).all()
# for session in sessions:
#     assert session.Date_Debut != '', f"Date_Debut non corrigé pour la session {session.Formation_Id}"
#     assert session.Date_Lim_Cand != '', f"Date_Lim_Cand non corrigé pour la session {session.Formation_Id}"
# print("Toutes les dates ont été vérifiées et corrigées si nécessaire")



# from sqlalchemy import create_engine, inspect
# from sqlalchemy.orm import sessionmaker
# from models import Sessions

# DATABASE_URL = "sqlite:///./simplon.db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
# db = SessionLocal()

# # Fonction pour nettoyer les dates invalides
# def clean_invalid_dates():
#     sessions = db.query(Sessions).all()
#     for session in sessions:
#         if isinstance(session.Date_Debut, str) and session.Date_Debut == '':
#             session.Date_Debut = None
#         if isinstance(session.Date_Lim_Cand, str) and session.Date_Lim_Cand == '':
#             session.Date_Lim_Cand = None
#         db.add(session)
#     db.commit()
#     print("Nettoyage des dates terminé")

# # Appel de la fonction de nettoyage
# clean_invalid_dates()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Sessions

DATABASE_URL = "sqlite:///./simplon.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def convert_dates_to_strings():
    sessions = db.query(Sessions).all()
    for session in sessions:
        if isinstance(session.Date_Debut, str) or session.Date_Debut is None:
            pass
        else:
            session.Date_Debut = session.Date_Debut.strftime("%Y-%m-%d")

        if isinstance(session.Date_Lim_Cand, str) or session.Date_Lim_Cand is None:
            pass
        else:
            session.Date_Lim_Cand = session.Date_Lim_Cand.strftime("%Y-%m-%d")

        db.add(session)
    db.commit()
    print("Conversion des dates en chaînes de caractères terminée")

convert_dates_to_strings()


