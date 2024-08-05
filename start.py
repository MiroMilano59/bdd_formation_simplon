import os
import time, subprocess
#from TRAITEMENT_MCF.download import download_json_data, URL
from TRAITEMENT_MCF.treat_files import load_data
# path = 'D:/DataScience/Projects/bdd_formation_simplon'
# import sys; sys.path.append(path)

def get_mcf_data():
    """
    This functions check 'Mon compte formation' fro new data and download them.

    No argument required
    """

    # BASIC SETTINGS & INITIALIZATION
    command = ['poetry', 'run', 'python', 'download.py']
    spider_directory = os.path.join(os.path.dirname(__file__),
                                    'TRAITEMENT_MCF')

    # RUNNING THE SCRAPER
    print("Récupération des données depuis Mon Compte Formation...")
    command = subprocess.run(command,
                             cwd = spider_directory,
                             text=True,
                             capture_output=True)

    # POTENTIAL EXCEPTION MANAGEMENT
    if command.returncode == 0:
        print("Synchronisation site MonCompteFormation réussie.")
        load_data()
        #print(command.stdout)
    else:
        print('Echec de la synchronisation avec MonCompteFromation')
        print(command.stderr)
    pass

def scrape_simplon_trainings():
    """
    Run the Scrapy spider named 'simplonspiderformation' to scrape trainings.

    This function takes no parameters and returns nothing.
    """

    # BASIC SETTINGS & INITIALIZATION
    command = ["scrapy", "crawl", "simplonspiderformation"]
    spider_directory = os.path.join(os.path.dirname(__file__),
                                    'SCRAPER',
                                    'crawl_simplon',
                                    'crawl_simplon')

    # RUNNING THE SCRAPER
    print("Scraping des formations sur le site web de Simplon.co...")
    command = subprocess.run(command,
                             cwd = spider_directory,
                             text=True,
                             capture_output=True,
                             encoding='utf-8')

    # POTENTIAL EXCEPTION MANAGEMENT
    if command.returncode == 0:
        print("Scraping des formations terminé avec succès.")
        #print(command.stdout)
    else:
        print('Le processus de scraping a rencontré des erreurs.')
        print(command.stderr)


if __name__ == '__main__':
    #print(type(URL))
    #print(URL)
    #scrape_simplon_trainings()
    get_mcf_data()
    scrape_simplon_trainings()
    #load_data()
    pass