# from sqlalchemy import create_engine, inspect
# from sqlalchemy.orm import sessionmaker
# from models import Sessions

# DATABASE_URL = "sqlite:///./simplon.db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
# db = SessionLocal()

# # Inspection des données
# sessions = db.query(Sessions).all()
# for session in sessions:
#     print(f"Formation_Id: {session.Formation_Id}, Date_Debut: {session.Date_Debut}, Date_Lim_Cand: {session.Date_Lim_Cand}")

# # Vérification des colonnes de la table sessions
# inspector = inspect(engine)
# if inspector.has_table("sessions"):
#     print("La table 'sessions' existe.")
#     columns = inspector.get_columns("sessions")
#     for column in columns:
#         print(f"Nom de la colonne: {column['name']}, Type: {column['type']}, Clé primaire: {column['primary_key']}")
# else:
#     print("La table 'sessions' n'existe pas.")


from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Sessions

DATABASE_URL = "sqlite:///./simplon.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Fonction pour afficher les valeurs de dates dans la table sessions
def show_date_values():
    sessions = db.query(Sessions).all()
    for session in sessions:
        print(f"Formation_Id: {session.Formation_Id}, Date_Debut: {session.Date_Debut}, Date_Lim_Cand: {session.Date_Lim_Cand}")

show_date_values()
