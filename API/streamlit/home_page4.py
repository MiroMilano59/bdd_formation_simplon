# import streamlit as st
# import pandas as pd
# import requests
# from io import BytesIO
# import plotly.express as px

# # Set page config
# st.set_page_config(page_title='Formations')

# # Title
# st.title('Bienvenue sur la page des formations')

# # API URLs
# API_URL_FORMATIONS = "http://127.0.0.1:8000/formations"
# API_URL_ORGANISMES = "http://127.0.0.1:8000/organismes"
# API_URL_RNCP = "http://127.0.0.1:8000/rncp"
# API_URL_RS = "http://127.0.0.1:8000/rs"
# API_URL_SESSIONS = "http://127.0.0.1:8000/sessions"
# API_URL_FORMACODES = "http://127.0.0.1:8000/formacodes"
# API_URL_NSF = "http://127.0.0.1:8000/nsf"

# # Function to fetch data from the FastAPI endpoint
# def get_data(api_url):
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status() 
#         data = response.json()
#         return pd.DataFrame(data)
#     except requests.exceptions.RequestException as e:
#         st.error(f"Erreur lors de la connexion à l'API : {e}")
#         return pd.DataFrame()  

# # Load data via the API
# df_simplon = get_data(API_URL_FORMATIONS)
# df_organismes = get_data(API_URL_ORGANISMES)
# df_rncp = get_data(API_URL_RNCP)
# df_rs = get_data(API_URL_RS)
# df_sessions = get_data(API_URL_SESSIONS)
# df_formacodes = get_data(API_URL_FORMACODES)
# df_nsf = get_data(API_URL_NSF)

# def telecharger_info(df):
#     demande_tele_info = st.checkbox("Souhaitez-vous télécharger les données ?", value=False)
#     if demande_tele_info:
#         @st.cache_data
#         def convert_df_to_csv(df):
#             return df.to_csv(index=False).encode('utf-8')

#         @st.cache_data
#         def convert_df_to_excel(df):
#             output = BytesIO()
#             with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#                 df.to_excel(writer, index=False, sheet_name='Sheet1')
#             processed_data = output.getvalue()
#             return processed_data

#         csv = convert_df_to_csv(df)
#         excel = convert_df_to_excel(df)

#         st.download_button(
#             label="Télécharger les résultats en CSV",
#             data=csv,
#             file_name='filtered_results.csv',
#             mime='text/csv',)

#         st.download_button(
#             label="Télécharger les résultats en Excel",
#             data=excel,
#             file_name='filtered_results.xlsx',
#             mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)


# st.sidebar.header('Limite de la recherche :')
# recherch_type_formation = st.sidebar.radio('Sélectionnez une catégorie :',
#                                            options=['Formation de Simplon',
#                                                     'Formation de moncompteformation',
#                                                     'Toutes les formations'])

# if recherch_type_formation == 'Formation de Simplon':
#     df_simplon = df_simplon[df_simplon['Simplon_Id'].str.strip() != '']

# elif recherch_type_formation == 'Formation de moncompteformation':
#     df_simplon = df_simplon[df_simplon['Simplon_Id'].str.strip() == '']

# ##############################
# # Formation Simplon
# ##############################
# if recherch_type_formation == 'Formation de Simplon':
#     simplon_ids = df_simplon['Id'].tolist()
    
#     # Filtrer les sessions basées sur les IDs de formation Simplon
#     df_sessions_simplon = df_sessions[df_sessions['formation_id'].isin(simplon_ids)]
    
#     st.write('Sessions de formation de Simplon:')
#     st.dataframe(df_sessions_simplon)
    
#     telecharger_info(df_sessions_simplon)

# ##############################
# # Formation moncompteformation
# ##############################
# if recherch_type_formation == 'Formation de moncompteformation':
#     activite_mcf = st.sidebar.radio('Sélectionnez une activité :',
#                                     options=['Voir et comparer les organismes concurents',
#                                              'Voir et comparer les RNCP',
#                                              'Voir et comparer les RS'])

# if activite_mcf == 'Voir et comparer les organismes concurents':
#     selected_organismes = st.multiselect('Sélectionnez les organismes à comparer', df_organismes['Nom'].unique())

#     # Filter the DataFrame based on the selected organismes
#     filtered_organismes = df_organismes[df_organismes['Nom'].isin(selected_organismes)]
#     siret_selected = filtered_organismes['Siret'].unique()
#     filtered_formations = df_simplon[df_simplon['Siret_OF'].isin(siret_selected)]
    
#     st.write('Formations associées aux organismes sélectionnés:')
#     st.dataframe(filtered_formations)
    
#     telecharger_info(filtered_formations)

# elif activite_mcf == 'Voir et comparer les RNCP':
#     selected_rncp = st.multiselect('Sélectionnez les RNCP à comparer', df_rncp['Libelle'].unique())

#     # Filter the DataFrame based on the selected RNCP
#     filtered_rncp = df_rncp[df_rncp['Libelle'].isin(selected_rncp)]

#     st.write('RNCP sélectionnés:')
#     st.dataframe(filtered_rncp)
#     telecharger_info(filtered_rncp)

# elif activite_mcf == 'Voir et comparer les RS':
#     selected_rs = st.multiselect('Sélectionnez les RS à comparer', df_rs['Libelle'].unique())

#     # Filter the DataFrame based on the selected RS
#     filtered_rs = df_rs[df_rs['Libelle'].isin(selected_rs)]

#     st.write('RS sélectionnés:')
#     st.dataframe(filtered_rs)
#     telecharger_info(filtered_rs)

# # Button to execute search
# if st.sidebar.button("Exécuter la recherche"):
#     st.dataframe(df_simplon)

#     st.header('Recherche de mots clés dans le Libele')
#     search_keyword = st.text_input('Entrez un mot clé :')

#     if search_keyword:
#         df_simplon = df_simplon[df_simplon['Libelle'].str.contains(search_keyword, case=False, na=False)]

#     row_count = df_simplon.shape[0]
#     st.write(f"Nombre de résultats : {row_count}")
#     st.dataframe(df_simplon)

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px

# Set page config
st.set_page_config(page_title='Formations')

# Title
st.title('Bienvenue sur la page des formations')

# API URLs
API_URL_FORMATIONS = "http://127.0.0.1:8000/formations"
API_URL_ORGANISMES = "http://127.0.0.1:8000/organismes"
API_URL_RNCP = "http://127.0.0.1:8000/rncp"
API_URL_RS = "http://127.0.0.1:8000/rs"
API_URL_SESSIONS = "http://127.0.0.1:8000/sessions"
API_URL_FORMACODES = "http://127.0.0.1:8000/formacodes"
API_URL_NSF = "http://127.0.0.1:8000/nsf"

# Function to fetch data from the FastAPI endpoint
def get_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la connexion à l'API : {e}")
        return pd.DataFrame()  

# Load data via the API
df_simplon = get_data(API_URL_FORMATIONS)
df_organismes = get_data(API_URL_ORGANISMES)
df_rncp = get_data(API_URL_RNCP)
df_rs = get_data(API_URL_RS)
df_sessions = get_data(API_URL_SESSIONS)
df_formacodes = get_data(API_URL_FORMACODES)
df_nsf = get_data(API_URL_NSF)

# Print the column names of df_sessions to debug the issue
st.write("Colonnes dans df_sessions:", df_sessions.columns.tolist())

def telecharger_info(df):
    demande_tele_info = st.checkbox("Souhaitez-vous télécharger les données ?", value=False)
    if demande_tele_info:
        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        @st.cache_data
        def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            return processed_data

        csv = convert_df_to_csv(df)
        excel = convert_df_to_excel(df)

        st.download_button(
            label="Télécharger les résultats en CSV",
            data=csv,
            file_name='filtered_results.csv',
            mime='text/csv',)

        st.download_button(
            label="Télécharger les résultats en Excel",
            data=excel,
            file_name='filtered_results.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)


st.sidebar.header('Limite de la recherche :')
recherch_type_formation = st.sidebar.radio('Sélectionnez une catégorie :',
                                           options=['Formation de Simplon',
                                                    'Formation de moncompteformation',
                                                    'Toutes les formations'])

if recherch_type_formation == 'Formation de Simplon':
    df_simplon = df_simplon[df_simplon['Simplon_Id'].str.strip() != '']

elif recherch_type_formation == 'Formation de moncompteformation':
    df_simplon = df_simplon[df_simplon['Simplon_Id'].str.strip() == '']

##############################
# Formation Simplon
##############################
if recherch_type_formation == 'Formation de Simplon':
    # Récupérer les IDs des formations Simplon
    simplon_ids = df_simplon['Id'].tolist()
    
    # Vérifier le nom de la colonne de formation dans df_sessions
    st.write("Colonnes dans df_sessions:", df_sessions.columns.tolist())
    
    # Remplacer 'Formation_Id' par le nom correct de la colonne
    df_sessions_simplon = df_sessions[df_sessions['Formation_Id'].isin(simplon_ids)]
    
    st.write('Sessions de formation de Simplon:')
    st.dataframe(df_sessions_simplon)
    
    telecharger_info(df_sessions_simplon)

##############################
# Formation moncompteformation
##############################
activite_mcf = None
if recherch_type_formation == 'Formation de moncompteformation':
    activite_mcf = st.sidebar.radio('Sélectionnez une activité :',
                                    options=['Voir et comparer les organismes concurents',
                                             'Voir et comparer les RNCP',
                                             'Voir et comparer les RS'])

if activite_mcf == 'Voir et comparer les organismes concurents':
    selected_organismes = st.multiselect('Sélectionnez les organismes à comparer', df_organismes['Nom'].unique())

    # Filter the DataFrame based on the selected organismes
    filtered_organismes = df_organismes[df_organismes['Nom'].isin(selected_organismes)]
    siret_selected = filtered_organismes['Siret'].unique()
    filtered_formations = df_simplon[df_simplon['Siret_OF'].isin(siret_selected)]
    
    st.write('Formations associées aux organismes sélectionnés:')
    st.dataframe(filtered_formations)
    
    telecharger_info(filtered_formations)

elif activite_mcf == 'Voir et comparer les RNCP':
    selected_rncp = st.multiselect('Sélectionnez les RNCP à comparer', df_rncp['Libelle'].unique())

    # Filter the DataFrame based on the selected RNCP
    filtered_rncp = df_rncp[df_rncp['Libelle'].isin(selected_rncp)]

    st.write('RNCP sélectionnés:')
    st.dataframe(filtered_rncp)
    telecharger_info(filtered_rncp)

elif activite_mcf == 'Voir et comparer les RS':
    selected_rs = st.multiselect('Sélectionnez les RS à comparer', df_rs['Libelle'].unique())

    # Filter the DataFrame based on the selected RS
    filtered_rs = df_rs[df_rs['Libelle'].isin(selected_rs)]

    st.write('RS sélectionnés:')
    st.dataframe(filtered_rs)
    telecharger_info(filtered_rs)

# Button to execute search
if st.sidebar.button("Exécuter la recherche"):
    st.dataframe(df_simplon)

    st.header('Recherche de mots clés dans le Libele')
    search_keyword = st.text_input('Entrez un mot clé :')

    if search_keyword:
        df_simplon = df_simplon[df_simplon['Libelle'].str.contains(search_keyword, case=False, na=False)]

    row_count = df_simplon.shape[0]
    st.write(f"Nombre de résultats : {row_count}")
    st.dataframe(df_simplon)
