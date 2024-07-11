import requests
import json
import dateparser

from urllib.parse import urlencode, quote_plus

base_url = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json"
query_params = {
    "select": "date_extract, nom_of, nom_departement, nom_region, type_referentiel, code_inventaire, intitule_certification, libelle_niveau_sortie_formation, code_formacode_1, code_formacode_2, code_formacode_3, code_formacode_4, code_formacode_5, libelle_code_formacode_principal, libelle_nsf_1, code_nsf_1, code_certifinfo, siret, intitule_formation, points_forts, nb_action, nb_session_active, nb_session_a_distance, nombre_heures_total_min, nombre_heures_total_max, nombre_heures_total_mean, frais_ttc_tot_min, frais_ttc_tot_max, frais_ttc_tot_mean, code_departement, code_region",
    "where": 'libelle_nsf_1 like "Informatique, traitement de l\'information, réseaux de transmission"',
    "limit": 5,
    "offset": 0,
    "timezone": "UTC",
    "include_links": "false",
    "include_app_metas": "false"
}

encoded_query_params = urlencode(query_params, quote_via=quote_plus)
URL = f"{base_url}?{encoded_query_params}"




formatData = "json" # data format
limitItem = 10 # -1 to retrieve all records
id_dataset = "moncompteformation_catalogueformation"
date_extract_item = "date_extract"
base_url_date = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/"

# URL to get last update date from MCF
URL_UPDATE_DATE = f"{base_url_date}{id_dataset}/records?select={date_extract_item}&limit=1&offset=0&timezone=UTC&include_links=false&include_app_metas=false"

# URL to get data from moncompteformation_catalogueformation
# URL = f"{base_url}{id_dataset}/exports/{formatData}?limit={limitItem}&timezone=UTC&use_labels=false&epsg=4326"

# File to store the last update date
date_file = 'last_update_date.txt'

def get_last_update_date_from_file():
    try:
        with open(date_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_last_update_date_on_file(date):
    with open(date_file, 'w') as file:
        file.write(date)



def get_last_update_date(url_to_last_date, item_to_extract):
    response = requests.get(url_to_last_date)
    response.raise_for_status()
    last_update_date = response.json()
    return last_update_date["results"][0][item_to_extract]


def download_json_data(url_to_json):

    try:
        last_update_date = get_last_update_date(url_to_last_date=URL_UPDATE_DATE, item_to_extract=date_extract_item)
        

        current_update_date = get_last_update_date_from_file()

        if dateparser.parse(last_update_date) > dateparser.parse(current_update_date):
            

            print(f"Nouvelle mise à jour trouvée : {last_update_date}")
            response = requests.get(url_to_json)
            response.raise_for_status()  # Vérifie si la requête a échoué
            data_formation_json = response.json()
            
            if not data_formation_json:
                print("Aucune donnée trouvée.")
            else:
                save_last_update_date_on_file(date=last_update_date)
                # Enregistrer les données dans un fichier JSON
                with open('TRAITEMENT_MCF/SRC/data_formation.json', 'w', encoding='utf-8') as json_file:
                    json.dump(data_formation_json, json_file, ensure_ascii=False, indent=4)
        else:
            print("Aucune nouvelle mise à jour")
                
    except requests.exceptions.RequestException as e:
        # Gère toutes les exceptions liées aux requêtes HTTP
        print(f"Erreur lors de la requête HTTP: {e}")
    except json.JSONDecodeError as e:
        # Gère les erreurs de décodage JSON
        print(f"Erreur lors du décodage JSON: {e}")
    except Exception as e:
        # Gère toutes les autres exceptions
        print(f"Une erreur est survenue: {e}")


if __name__ == "__main__":
   download_json_data(url_to_json=URL)