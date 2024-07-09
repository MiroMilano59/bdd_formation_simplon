import requests
import json


formatData = "json" # data format
limitItem = 50 # -1 to retrieve all records
id_dataset = "moncompteformation_catalogueformation"
base_url = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/"


# URL to get data from moncompteformation_catalogueformation
URL = f"{base_url}{id_dataset}/exports/{formatData}?limit={limitItem}&timezone=UTC&use_labels=false&epsg=4326"



try:
    response = requests.get(URL)
    response.raise_for_status()  # Vérifie si la requête a échoué
    data_formation_json = response.json()
    
    # Vérifier si la réponse contient des données valides
    if not data_formation_json:
        print("Aucune donnée trouvée.")
    else:
        # Enregistrer les données dans un fichier JSON
        with open('TRAITEMENT_MCF/SRC/data_formation.json', 'w', encoding='utf-8') as json_file:
            json.dump(data_formation_json, json_file, ensure_ascii=False, indent=4)

except requests.exceptions.RequestException as e:
    # Gère toutes les exceptions liées aux requêtes HTTP
    print(f"Erreur lors de la requête HTTP: {e}")
except json.JSONDecodeError as e:
    # Gère les erreurs de décodage JSON
    print(f"Erreur lors du décodage JSON: {e}")
except Exception as e:
    # Gère toutes les autres exceptions
    print(f"Une erreur est survenue: {e}")