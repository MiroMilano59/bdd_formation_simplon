# home_page.py
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Get the absolute path to the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(BASE_DIR, '..', 'data', 'formation7.csv')

# Load the CSV data
df_simplon = pd.read_csv(csv_file_path)

# Streamlit UI setup
st.set_page_config(page_title='Formations')
st.header('Outil de recherche de formation')

# Sidebar setup
st.sidebar.header('Limite de la recherche :')
recherch_type = st.sidebar.radio('Sélectionnez une catégorie :',
                          options=['Formation de Simplon',
                                   'Formation de moncompteformation',
                                   'Toutes les formations'])

st.sidebar.header('Nom département')
department_formation_selected = st.sidebar.multiselect('Choisissez une ou des département(s) :',
                                          options=['Auvergne-Rhône-Alpes',
                                                   'Grand Est',
                                                   'Grand Ouest',
                                                   'Hauts-de-France',
                                                   'Île-de-France',
                                                   'Nouvelle-Aquitaine',
                                                   'Provence-Alpes-Cote d Azur',
                                                   'Occitanie',
                                                   'Outre-mer'])

st.sidebar.header('Code certification')
certification_formation_selected = st.sidebar.multiselect('Choisissez une ou des code de certification :',
                                          options=['RNCP',
                                                   'RS'])

st.sidebar.header('Option de la formation')
option_formation_selected = st.sidebar.multiselect('Choisissez une ou des options de la formation :',
                                          options=['Alternance',
                                                   'Distance',
                                                   'Que femme',])

for option in option_formation_selected:
    if option == 'Alternance':
        df_simplon = df_simplon[df_simplon['Alternance'] == True] 
    elif option == 'Distance':
        df_simplon = df_simplon[df_simplon['Distance'] == True]  
    elif option == 'Que femme':
        df_simplon = df_simplon[df_simplon['Que femme'] == True]


if department_formation_selected:
    df_simplon = df_simplon[df_simplon['Nom_Dept'].isin(department_formation_selected)]

# # Filter based on certification codes
# if 'RNCP' in certification_formation_selected:
#     df_simplon = df_simplon[df_simplon['Certification'] == 'RNCP']
# if 'RS' in certification_formation_selected:
#     df_simplon = df_simplon[df_simplon['Certification'] == 'RS']

# Display the filtered dataframe on button click
if st.sidebar.button("Exécuter la recherche"):
    st.dataframe(df_simplon)

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

    csv = convert_df_to_csv(df_simplon)
    excel = convert_df_to_excel(df_simplon)

    st.download_button(
        label="Télécharger les résultats en CSV",
        data=csv,
        file_name='filtered_results.csv',
        mime='text/csv',
    )

    st.download_button(
        label="Télécharger les résultats en Excel",
        data=excel,
        file_name='filtered_results.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
