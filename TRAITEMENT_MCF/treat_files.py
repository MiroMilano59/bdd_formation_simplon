import pandas as pd

# DATA SOURCES
file = "TRAITEMENT_MCF\SRC\data_formation.json"  # Path to the most recent json
simplon = '79279132900016'                       # SIRET of "simplon.co"

# DATA LOADING
def load_data():
    """
    Open a '.json' file (from `moncompteformation`) and save data in database.

    No parameters and nothing returned (just data added to thedatabase)"""
    df = pd.read_json(file)
    print(df.sort_values(by=['date_extract'])[:10])
    print(df.sort_values(by=['date_extract'])[-10:])



load_data()