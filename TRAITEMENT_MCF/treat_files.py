import pandas as pd

# DATA SOURCES
file = "TRAITEMENT_MCF\SRC\data_formation.json"

# DATA LOADING
def load_data():
    """
    Open a json file (from `moncompteformation`) and save data in database

    Parameter(s) : None

    Retruns : Nothing (just add json data to the simplon database)"""
    df = pd.read_json(file)
    print(df.sort_values(by=['date_extract'])[:10])
    print(df.sort_values(by=['date_extract'])[-10:])


load_data()