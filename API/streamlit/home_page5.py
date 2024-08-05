# import streamlit as st
# import pandas as pd
# import aiohttp
# import asyncio
# from io import BytesIO
# import plotly.express as px

# # Set page config
# st.set_page_config(page_title='Formations', layout='wide')

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

# # Function to fetch data from the FastAPI endpoint asynchronously
# async def fetch_data(session, url):
#     async with session.get(url) as response:
#         return await response.json()

# @st.cache_data(ttl=600)
# def load_data(api_url):
#     async def get_data(api_url):
#         async with aiohttp.ClientSession() as session:
#             data = await fetch_data(session, api_url)
#             return pd.DataFrame(data)
#     return asyncio.run(get_data(api_url))

# # Load data via the API
# df_formations = load_data(API_URL_FORMATIONS)
# df_organismes = load_data(API_URL_ORGANISMES)
# df_rncp = load_data(API_URL_RNCP)
# df_rs = load_data(API_URL_RS)
# df_sessions = load_data(API_URL_SESSIONS)
# df_formacodes = load_data(API_URL_FORMACODES)
# df_nsf = load_data(API_URL_NSF)

# # Function to download data
# def telecharger_info(df, key_suffix):
#     demande_tele_info = st.checkbox("Souhaitez-vous télécharger les données ?", value=False, key=f'download_{key_suffix}')
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
#             mime='text/csv',
#             key=f'download_csv_{key_suffix}')

#         st.download_button(
#             label="Télécharger les résultats en Excel",
#             data=excel,
#             file_name='filtered_results.xlsx',
#             mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#             key=f'download_excel_{key_suffix}')

# # Sidebar for navigation
# st.sidebar.header('Navigation')
# page = st.sidebar.radio('Sélectionnez une page :',
#                         options=['Accueil', 'Formation de Simplon', 'Formation de Mon Compte Formation', 'Toutes les Formations'])

# if page == 'Accueil':
#     st.header('Statistiques Clés')

#     # Lier les formations et les sessions
#     df_sessions_formations = pd.merge(df_sessions, df_formations, left_on='Formation_Id', right_on='Id', how='left')

#     # Calcul des statistiques globales
#     total_formations = df_formations.shape[0]
#     total_organismes = df_organismes.shape[0]

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Nombre total de formations", total_formations)
#     col3.metric("Nombre total d'organismes", total_organismes)

#     # Pie chart des RNCP
#     fig_rncp = px.pie(df_rncp, names='Libelle', title='Répartition des RNCP')
#     st.plotly_chart(fig_rncp)

#     # Pie chart des RS
#     fig_rs = px.pie(df_rs, names='Libelle', title='Répartition des RS')
#     st.plotly_chart(fig_rs)

# elif page == 'Formation de Simplon':
#     st.header('Formations de Simplon')

#     simplon_activity = st.sidebar.radio('Sélectionnez une activité :',
#                                         options=['Formations et Sessions', 'Recherche par mot clé', 'Voir les sessions par formation', 'Voir les sessions par département', 'Voir les sessions en alternance', 'Voir les sessions en distanciel'])

#     # Filtrer les formations de Simplon
#     simplon_formations = df_formations[df_formations['Simplon_Id'].notnull() & (df_formations['Simplon_Id'] != '')]
#     df_sessions_simplon = pd.merge(df_sessions, simplon_formations, left_on='Formation_Id', right_on='Id')

#     if simplon_activity == 'Formations et Sessions':
#         # Afficher les formations et les sessions de Simplon
#         st.subheader('Formations de Simplon')
#         st.dataframe(simplon_formations)

#         st.subheader('Sessions de formation de Simplon')
#         st.dataframe(df_sessions_simplon)

#         telecharger_info(simplon_formations, 'formations_simplon')
#         telecharger_info(df_sessions_simplon, 'sessions_simplon')

#     elif simplon_activity == 'Recherche par mot clé':
#         # Recherche par mot-clé
#         st.subheader('Recherche par mot clé dans les formations de Simplon')
#         search_keyword_simplon = st.text_input('Entrez un mot clé :', key='search_keyword_simplon')

#         if search_keyword_simplon:
#             df_filtered_simplon = simplon_formations[simplon_formations['Libelle'].str.contains(search_keyword_simplon, case=False, na=False)]
#             st.write(f"Nombre de résultats : {df_filtered_simplon.shape[0]}")
#             st.dataframe(df_filtered_simplon)

#             df_filtered_sessions = df_sessions_simplon[df_sessions_simplon['Formation_Id'].isin(df_filtered_simplon['Id'].tolist())]
#             st.write(f"Nombre de sessions : {df_filtered_sessions.shape[0]}")
#             st.dataframe(df_filtered_sessions)

#             telecharger_info(df_filtered_simplon, 'filtered_simplon')
#             telecharger_info(df_filtered_sessions, 'filtered_sessions')

#     elif simplon_activity == 'Voir les sessions par formation':
#         # Activité : Voir les sessions par formation Simplon
#         st.subheader('Sessions par formation de Simplon')
#         formation_simplon_libelle = st.selectbox('Sélectionnez une formation Simplon :', options=simplon_formations['Libelle'].unique())
#         if formation_simplon_libelle:
#             selected_formation_id = simplon_formations[simplon_formations['Libelle'] == formation_simplon_libelle]['Id'].iloc[0]
#             df_selected_sessions = df_sessions_simplon[df_sessions_simplon['Formation_Id'] == selected_formation_id]
#             st.dataframe(df_selected_sessions)

#             telecharger_info(df_selected_sessions, 'selected_sessions_simplon')

#     elif simplon_activity == 'Voir les sessions par département':
#         # Activité : Voir les sessions par département
#         st.subheader('Sessions par département pour les formations de Simplon')
#         nom_dept_simplon = st.selectbox('Sélectionnez un département :', options=df_sessions_simplon['Nom_Dept'].unique())
#         if nom_dept_simplon:
#             df_sessions_by_dept_simplon = df_sessions_simplon[df_sessions_simplon['Nom_Dept'] == nom_dept_simplon]
#             st.dataframe(df_sessions_by_dept_simplon)

#             telecharger_info(df_sessions_by_dept_simplon, 'sessions_dept_simplon')

#     elif simplon_activity == 'Voir les sessions en alternance':
#         # Activité : Voir les sessions en alternance
#         st.subheader('Sessions en alternance pour les formations de Simplon')
#         df_sessions_alternance = df_sessions_simplon[df_sessions_simplon['Type'] == 'Alternance']
#         st.dataframe(df_sessions_alternance)

#         telecharger_info(df_sessions_alternance, 'sessions_alternance')

#     elif simplon_activity == 'Voir les sessions en distanciel':
#         # Activité : Voir les sessions en distanciel
#         st.subheader('Sessions en distanciel pour les formations de Simplon')
#         df_sessions_distanciel = df_sessions_simplon[df_sessions_simplon['Mode'] == 'Distanciel']
#         st.dataframe(df_sessions_distanciel)

#         telecharger_info(df_sessions_distanciel, 'sessions_distanciel')

# elif page == 'Formation de Mon Compte Formation':
#     st.header('Formations de Mon Compte Formation')

#     activite_mcf = st.sidebar.radio('Sélectionnez une activité :',
#                                     options=['Voir et comparer les organismes concurents',
#                                             'Voir et comparer les RNCP',
#                                             'Voir et comparer les RS',
#                                             'Sessions par département'])

#     if activite_mcf == 'Voir et comparer les organismes concurents':
#         selected_organismes = st.multiselect('Sélectionnez les organismes à comparer', df_organismes['Nom'].unique())
#         df_formations_nettoyer = df_formations[df_formations['Simplon_Id'].str.strip() == '']

#         # Filter the DataFrame based on the selected organismes
#         filtered_organismes = df_organismes[df_organismes['Nom'].isin(selected_organismes)]
#         siret_selected = filtered_organismes['Siret'].unique()
#         filtered_formations = df_formations_nettoyer[df_formations_nettoyer['Siret_OF'].isin(siret_selected)]

#         st.write('Formations associées aux organismes sélectionnés:')
#         st.dataframe(filtered_formations)

#         telecharger_info(filtered_formations, 'filtered_organismes')

#     if activite_mcf == 'Voir et comparer les RNCP':
#         selected_rncp = st.multiselect('Sélectionnez les RNCP à comparer', df_rncp['Libelle'].unique())
#         filtered_rncp = df_rncp[df_rncp['Libelle'].isin(selected_rncp)]

#         st.write('RNCP sélectionnés:')
#         st.dataframe(filtered_rncp)

#         telecharger_info(filtered_rncp, 'rncp')

#     elif activite_mcf == 'Voir et comparer les RS':
#         selected_rs = st.multiselect('Sélectionnez les RS à comparer', df_rs['Libelle'].unique())
#         filtered_rs = df_rs[df_rs['Libelle'].isin(selected_rs)]

#         st.write('RS sélectionnés:')
#         st.dataframe(filtered_rs)

#         telecharger_info(filtered_rs, 'rs')

#     elif activite_mcf == 'Sessions par département':
#         # Activité : Voir les sessions par département pour les formations de Mon Compte Formation
#         st.subheader('Sessions par département pour les formations de Mon Compte Formation')
#         moncompte_formations = df_formations[df_formations['Simplon_Id'].isnull() | (df_formations['Simplon_Id'] == '')]
#         df_sessions_moncompte = df_sessions[df_sessions['Formation_Id'].isin(moncompte_formations['Id'].tolist())]
#         nom_dept_moncompte = st.selectbox('Sélectionnez un département :', options=df_sessions_moncompte['Nom_Dept'].unique())
#         if nom_dept_moncompte:
#             df_sessions_by_dept_moncompte = df_sessions_moncompte[df_sessions_moncompte['Nom_Dept'] == nom_dept_moncompte]
#             st.dataframe(df_sessions_by_dept_moncompte)

#             telecharger_info(df_sessions_by_dept_moncompte, 'sessions_dept_moncompte')

# elif page == 'Toutes les Formations':
#     st.header('Toutes les Formations')

#     st.subheader('Comparaison des formations de Simplon et de Mon Compte Formation')

#     simplon_formations = df_formations[df_formations['Simplon_Id'].notnull() & (df_formations['Simplon_Id'] != '')]
#     moncompte_formations = df_formations[df_formations['Simplon_Id'].isnull() | (df_formations['Simplon_Id'] == '')]

#     st.write('Formations de Simplon')
#     st.dataframe(simplon_formations)

#     st.write('Formations de Mon Compte Formation')
#     st.dataframe(moncompte_formations)

#     selected_simplon_libelles = st.multiselect('Sélectionnez les formations de Simplon à comparer', simplon_formations['Libelle'].unique())
#     selected_moncompte_libelles = st.multiselect('Sélectionnez les formations de Mon Compte Formation à comparer', moncompte_formations['Libelle'].unique())

#     if selected_simplon_libelles and selected_moncompte_libelles:
#         df_selected_simplon = simplon_formations[simplon_formations['Libelle'].isin(selected_simplon_libelles)]
#         df_selected_moncompte = moncompte_formations[moncompte_formations['Libelle'].isin(selected_moncompte_libelles)]

#         st.write('Comparaison des formations sélectionnées de Simplon')
#         st.dataframe(df_selected_simplon)

#         st.write('Comparaison des formations sélectionnées de Mon Compte Formation')
#         st.dataframe(df_selected_moncompte)

#         combined_df = pd.concat([df_selected_simplon, df_selected_moncompte])
#         st.write('Comparaison combinée des formations sélectionnées')
#         st.dataframe(combined_df)

#         telecharger_info(combined_df, 'comparison')

#     # Activité : Voir les sessions par département pour toutes les formations
#     st.subheader('Sessions par département pour toutes les formations')
#     nom_dept_all = st.selectbox('Sélectionnez un département :', options=df_sessions['Nom_Dept'].unique())
#     if nom_dept_all:
#         df_sessions_by_dept_all = df_sessions[df_sessions['Nom_Dept'] == nom_dept_all]
#         st.dataframe(df_sessions_by_dept_all)

#         telecharger_info(df_sessions_by_dept_all, 'sessions_dept_all')



import streamlit as st
import pandas as pd
import aiohttp
import asyncio
from io import BytesIO
import plotly.express as px

# Set page config
st.set_page_config(page_title='Formations', layout='wide')

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

# Function to fetch data from the FastAPI endpoint asynchronously
async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()

@st.cache_data(ttl=600)
def load_data(api_url):
    async def get_data(api_url):
        async with aiohttp.ClientSession() as session:
            data = await fetch_data(session, api_url)
            return pd.DataFrame(data)
    return asyncio.run(get_data(api_url))

# Load data via the API
df_formations = load_data(API_URL_FORMATIONS)
df_organismes = load_data(API_URL_ORGANISMES)
df_rncp = load_data(API_URL_RNCP)
df_rs = load_data(API_URL_RS)
df_sessions = load_data(API_URL_SESSIONS)
df_formacodes = load_data(API_URL_FORMACODES)
df_nsf = load_data(API_URL_NSF)

# Function to download data
def telecharger_info(df, key_suffix):
    demande_tele_info = st.checkbox("Souhaitez-vous télécharger les données ?", value=False, key=f'download_{key_suffix}')
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
            mime='text/csv',
            key=f'download_csv_{key_suffix}')

        st.download_button(
            label="Télécharger les résultats en Excel",
            data=excel,
            file_name='filtered_results.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            key=f'download_excel_{key_suffix}')

# Sidebar for navigation
st.sidebar.header('Navigation')
page = st.sidebar.radio('Sélectionnez une page :',
                        options=['Accueil', 'Formation de Simplon', 'Formation de Mon Compte Formation', 'Toutes les Formations'])

if page == 'Accueil':
    st.header('Statistiques Clés')

    # Lier les formations et les sessions
    df_sessions_formations = pd.merge(df_sessions, df_formations, left_on='Formation_Id', right_on='Id', how='left')

    # Calcul des statistiques globales
    total_formations = df_formations.shape[0]
    total_organismes = df_organismes.shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre total de formations", total_formations)
    col3.metric("Nombre total d'organismes", total_organismes)

    # Pie chart des RNCP
    fig_rncp = px.pie(df_rncp, names='Libelle', title='Répartition des RNCP')
    st.plotly_chart(fig_rncp)

    # Pie chart des RS
    fig_rs = px.pie(df_rs, names='Libelle', title='Répartition des RS')
    st.plotly_chart(fig_rs)

elif page == 'Formation de Simplon':
    st.header('Formations de Simplon')

    simplon_activity = st.sidebar.radio('Sélectionnez une activité :',
                                        options=['Formations et Sessions', 'Recherche par mot clé', 'Voir les sessions par formation', 'Voir les sessions par département', 'Voir les sessions en alternance', 'Voir les sessions en distanciel'])

    # Filtrer les formations de Simplon
    simplon_formations = df_formations[df_formations['Simplon_Id'].notnull() & (df_formations['Simplon_Id'] != '')]
    df_sessions_simplon = pd.merge(df_sessions, simplon_formations, left_on='Formation_Id', right_on='Id')

    if simplon_activity == 'Formations et Sessions':
        # Afficher les formations et les sessions de Simplon
        st.subheader('Formations de Simplon')
        st.dataframe(simplon_formations)

        st.subheader('Sessions de formation de Simplon')
        st.dataframe(df_sessions_simplon)

        telecharger_info(simplon_formations, 'formations_simplon')
        telecharger_info(df_sessions_simplon, 'sessions_simplon')

    elif simplon_activity == 'Recherche par mot clé':
        # Recherche par mot-clé
        st.subheader('Recherche par mot clé dans les formations de Simplon')
        search_keyword_simplon = st.text_input('Entrez un mot clé :', key='search_keyword_simplon')

        if search_keyword_simplon:
            df_filtered_simplon = simplon_formations[simplon_formations['Libelle'].str.contains(search_keyword_simplon, case=False, na=False)]
            st.write(f"Nombre de résultats : {df_filtered_simplon.shape[0]}")
            st.dataframe(df_filtered_simplon)

            df_filtered_sessions = df_sessions_simplon[df_sessions_simplon['Formation_Id'].isin(df_filtered_simplon['Id'].tolist())]
            st.write(f"Nombre de sessions : {df_filtered_sessions.shape[0]}")
            st.dataframe(df_filtered_sessions)

            telecharger_info(df_filtered_simplon, 'filtered_simplon')
            telecharger_info(df_filtered_sessions, 'filtered_sessions')

    elif simplon_activity == 'Voir les sessions par formation':
        # Activité : Voir les sessions par formation Simplon
        st.subheader('Sessions par formation de Simplon')
        formation_simplon_libelle = st.selectbox('Sélectionnez une formation Simplon :', options=simplon_formations['Libelle'].unique())
        if formation_simplon_libelle:
            selected_formation_id = simplon_formations[simplon_formations['Libelle'] == formation_simplon_libelle]['Id'].iloc[0]
            df_selected_sessions = df_sessions_simplon[df_sessions_simplon['Formation_Id'] == selected_formation_id]
            st.dataframe(df_selected_sessions)

            telecharger_info(df_selected_sessions, 'selected_sessions_simplon')

    elif simplon_activity == 'Voir les sessions par département':
        # Activité : Voir les sessions par département
        st.subheader('Sessions par département pour les formations de Simplon')
        nom_dept_simplon = st.selectbox('Sélectionnez un département :', options=df_sessions_simplon['Nom_Dept'].unique())
        if nom_dept_simplon:
            df_sessions_by_dept_simplon = df_sessions_simplon[df_sessions_simplon['Nom_Dept'] == nom_dept_simplon]
            st.dataframe(df_sessions_by_dept_simplon)

            telecharger_info(df_sessions_by_dept_simplon, 'sessions_dept_simplon')

    elif simplon_activity == 'Voir les sessions en alternance':
        # Activité : Voir les sessions en alternance
        st.subheader('Sessions en alternance pour les formations de Simplon')
        df_sessions_alternance = df_sessions_simplon[df_sessions_simplon['alternance'] == 1]
        st.dataframe(df_sessions_alternance)

        telecharger_info(df_sessions_alternance, 'sessions_alternance')

    elif simplon_activity == 'Voir les sessions en distanciel':
        # Activité : Voir les sessions en distanciel
        st.subheader('Sessions en distanciel pour les formations de Simplon')
        df_sessions_distanciel = df_sessions_simplon[df_sessions_simplon['distanciel'] == 1]
        st.dataframe(df_sessions_distanciel)

        telecharger_info(df_sessions_distanciel, 'sessions_distanciel')

elif page == 'Formation de Mon Compte Formation':
    st.header('Formations de Mon Compte Formation')

    activite_mcf = st.sidebar.radio('Sélectionnez une activité :',
                                    options=['Voir et comparer les organismes concurents',
                                            'Voir et comparer les RNCP',
                                            'Voir et comparer les RS',
                                            'Sessions par département'])

    if activite_mcf == 'Voir et comparer les organismes concurents':
        selected_organismes = st.multiselect('Sélectionnez les organismes à comparer', df_organismes['Nom'].unique())
        df_formations_nettoyer = df_formations[df_formations['Simplon_Id'].str.strip() == '']

        # Filter the DataFrame based on the selected organismes
        filtered_organismes = df_organismes[df_organismes['Nom'].isin(selected_organismes)]
        siret_selected = filtered_organismes['Siret'].unique()
        filtered_formations = df_formations_nettoyer[df_formations_nettoyer['Siret_OF'].isin(siret_selected)]

        st.write('Formations associées aux organismes sélectionnés:')
        st.dataframe(filtered_formations)

        telecharger_info(filtered_formations, 'filtered_organismes')

    if activite_mcf == 'Voir et comparer les RNCP':
        selected_rncp = st.multiselect('Sélectionnez les RNCP à comparer', df_rncp['Libelle'].unique())
        filtered_rncp = df_rncp[df_rncp['Libelle'].isin(selected_rncp)]

        st.write('RNCP sélectionnés:')
        st.dataframe(filtered_rncp)

        telecharger_info(filtered_rncp, 'rncp')

    elif activite_mcf == 'Voir et comparer les RS':
        selected_rs = st.multiselect('Sélectionnez les RS à comparer', df_rs['Libelle'].unique())
        filtered_rs = df_rs[df_rs['Libelle'].isin(selected_rs)]

        st.write('RS sélectionnés:')
        st.dataframe(filtered_rs)

        telecharger_info(filtered_rs, 'rs')

    elif activite_mcf == 'Sessions par département':
        # Activité : Voir les sessions par département pour les formations de Mon Compte Formation
        st.subheader('Sessions par département pour les formations de Mon Compte Formation')
        moncompte_formations = df_formations[df_formations['Simplon_Id'].isnull() | (df_formations['Simplon_Id'] == '')]
        df_sessions_moncompte = df_sessions[df_sessions['Formation_Id'].isin(moncompte_formations['Id'].tolist())]
        nom_dept_moncompte = st.selectbox('Sélectionnez un département :', options=df_sessions_moncompte['Nom_Dept'].unique())
        if nom_dept_moncompte:
            df_sessions_by_dept_moncompte = df_sessions_moncompte[df_sessions_moncompte['Nom_Dept'] == nom_dept_moncompte]
            st.dataframe(df_sessions_by_dept_moncompte)

            telecharger_info(df_sessions_by_dept_moncompte, 'sessions_dept_moncompte')

elif page == 'Toutes les Formations':
    st.header('Toutes les Formations')

    toutes_activites = st.sidebar.radio('Sélectionnez une activité :',
                                        options=['Comparaison des formations', 'Voir et comparer les RNCP', 'Voir et comparer les RS'])

    if toutes_activites == 'Comparaison des formations':
        st.subheader('Comparaison des formations de Simplon et de Mon Compte Formation')

        simplon_formations = df_formations[df_formations['Simplon_Id'].notnull() & (df_formations['Simplon_Id'] != '')]
        moncompte_formations = df_formations[df_formations['Simplon_Id'].isnull() | (df_formations['Simplon_Id'] == '')]

        st.write('Formations de Simplon')
        st.dataframe(simplon_formations)

        st.write('Formations de Mon Compte Formation')
        st.dataframe(moncompte_formations)

        selected_simplon_libelles = st.multiselect('Sélectionnez les formations de Simplon à comparer', simplon_formations['Libelle'].unique())
        selected_moncompte_libelles = st.multiselect('Sélectionnez les formations de Mon Compte Formation à comparer', moncompte_formations['Libelle'].unique())

        if selected_simplon_libelles and selected_moncompte_libelles:
            df_selected_simplon = simplon_formations[simplon_formations['Libelle'].isin(selected_simplon_libelles)]
            df_selected_moncompte = moncompte_formations[moncompte_formations['Libelle'].isin(selected_moncompte_libelles)]

            st.write('Comparaison des formations sélectionnées de Simplon')
            st.dataframe(df_selected_simplon)

            st.write('Comparaison des formations sélectionnées de Mon Compte Formation')
            st.dataframe(df_selected_moncompte)

            combined_df = pd.concat([df_selected_simplon, df_selected_moncompte])
            st.write('Comparaison combinée des formations sélectionnées')
            st.dataframe(combined_df)

            telecharger_info(combined_df, 'comparison')

        # Activité : Voir les sessions par département pour toutes les formations
        st.subheader('Sessions par département pour toutes les formations')
        nom_dept_all = st.selectbox('Sélectionnez un département :', options=df_sessions['Nom_Dept'].unique())
        if nom_dept_all:
            df_sessions_by_dept_all = df_sessions[df_sessions['Nom_Dept'] == nom_dept_all]
            st.dataframe(df_sessions_by_dept_all)

            telecharger_info(df_sessions_by_dept_all, 'sessions_dept_all')

    elif toutes_activites == 'Voir et comparer les RNCP':
        st.subheader('Voir et comparer les RNCP')

        selected_rncp = st.multiselect('Sélectionnez les RNCP à comparer', df_rncp['Libelle'].unique())
        filtered_rncp = df_rncp[df_rncp['Libelle'].isin(selected_rncp)]

        st.write('RNCP sélectionnés:')
        st.dataframe(filtered_rncp)

        if not filtered_rncp.empty:
            rncp_codes = filtered_rncp['Code'].unique()
            formations_rncp = df_formacodes[df_formacodes['Code'].isin(rncp_codes)]
            formations_associees = df_formations[df_formations['Id'].isin(formations_rncp['formation_id'])]

            st.write('Formations associées aux RNCP sélectionnés:')
            st.dataframe(formations_associees)

            telecharger_info(formations_associees, 'formations_rncp')

    elif toutes_activites == 'Voir et comparer les RS':
        st.subheader('Voir et comparer les RS')

        selected_rs = st.multiselect('Sélectionnez les RS à comparer', df_rs['Libelle'].unique())
        filtered_rs = df_rs[df_rs['Libelle'].isin(selected_rs)]

        st.write('RS sélectionnés:')
        st.dataframe(filtered_rs)

        if not filtered_rs.empty:
            rs_codes = filtered_rs['Code'].unique()
            formations_rs = df_formacodes[df_formacodes['Code'].isin(rs_codes)]
            formations_associees_rs = df_formations[df_formations['Id'].isin(formations_rs['formation_id'])]

            st.write('Formations associées aux RS sélectionnés:')
            st.dataframe(formations_associees_rs)

            telecharger_info(formations_associees_rs, 'formations_rs')
