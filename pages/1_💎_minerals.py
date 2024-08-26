import streamlit as st
import pandas as pd
import requests
import json
import tempfile 
import re

######################################################### Functions #########################################################

#Functions to check if the response is valid JSON

def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

# function to make html more readable

def remove_sup_sub_tags(chemical_formula):
    # Replace <sub> with _ and </sub> with nothing
    formula = re.sub(r'<sub>', '_', chemical_formula)
    # Replace <sup> and </sup> with nothing
    formula = re.sub(r'<sub>(.*?)</sub>', r'_\1', chemical_formula)
    # Replace <sup>...</sup> with ^ 
    formula = re.sub(r'<sup>(.*?)</sup>', r'^\1', formula)
    # Replace &middot
    formula = formula.replace('&middot;', '·')
    return formula

######################################################### text and information #############################################

header = 'An Overview of the Most Important Minerals'
subheader_1='Welcome!'
subheader_2='Select the mineral and the information you want to get'
subheader_3='Request the Information'
subheader_4='Results:'
subheader_5='Download Results'
info_1 =('This app can be used to get information about the most important minerals in geoscience. '
        'The information provided here is requested from mindat.org and only information for minerals '
        'which are approved by the International Mineralogical Association (IMA) are available. '
        'The shortcode and formula for the minerals are the IMA-shortcode and the IMA-formula. '
        'Your selected information will be requested from Mindat.org. If you want to explore more '
        'information about minerals, you can visit [Mindat.org](https://www.mindat.org).')
info_2 ='If you want, you can download the displayed results for the chosen mineral as a JSON file.'
label_selectbox_1='Select a mineral:'
label_selectbox_3='Select a second mineral:'
label_selectbox_4='Select a third mineral:'
label_selectbox_2='Select fields:'
label_button_2='Download selected information as JSON'

st.header('Get Information about a specific mineral')
st.markdown(info_1)
st.divider()
st.subheader(subheader_2)

######################################################### Parameters API request ##############################################################

key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"

######################################################### Definition of the Important minerals and fields ###########################################################

url_1 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/important_minerals.csv"
url_2 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/listshort.csv"
url_3 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/listall.csv"
url_4 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/fieldsshort.json"
url_5 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/fieldsall.json"

important_minerals = pd.read_csv(url_1)

list_short = pd.read_csv(url_2)

list_all = pd.read_csv(url_3)

########################################################### Field mapping #######################################################################

response = requests.get(url_4)
field_mapping = response.json()

response = requests.get(url_5)
field_mapping_all = response.json()

mapped_fields=list(field_mapping.keys())
mapped_fields_results = {v: k for k, v in field_mapping.items()}

mapped_fields_all=list(field_mapping_all.keys())
mapped_fields_results_all = {v: k for k, v in field_mapping_all.items()}

########################################## User Input ######################################

col1, col2 = st.columns(2)

# select minerals
with col1:
    minerals=st.multiselect('Select minerals:',important_minerals)

# select fields
with col2:
    multiselect = st.multiselect(label=label_selectbox_2, options=mapped_fields)

options_select=['Select fields manually','Select all','Use all fields from Mindat.org/geomaterials']
radio_selection = st.radio('', options=options_select)

# checkbox link 

show_link=st.checkbox('Show the Mindat.org links for the selected minerals')

st.divider()
st.subheader(subheader_4)

if radio_selection == 'Select all':
    selection = list_short  # Ensure this is a list of column names
    api_fields = [field_mapping.get(field) for field in selection]
    api_fields.insert(0, 'name')
    api_fields.insert(1, 'id')
    api_fields.insert(2, 'ima_formula')
elif radio_selection == 'Use all fields from Mindat.org/geomaterials':
    selection = list_all  # Ensure this is a list of column names
    api_fields = [field_mapping_all.get(field) for field in selection]
    api_fields.insert(0, 'name')
    api_fields.insert(1, 'id')
    api_fields.insert(2, 'ima_formula')
elif radio_selection == 'Select fields manually':
    selection = multiselect
    api_fields = [field_mapping.get(field) for field in selection]
    api_fields.insert(0, 'name')
    api_fields.insert(1, 'id')
    api_fields.insert(2, 'ima_formula')
else:
    st.write("Please select an option to proceed.")
   
############################################################ API Request ########################################################

all_results = []

for mineral in minerals:
    
    params = {"name": mineral, "ima_status": "APPROVED", "format": "json"}
    headers = {'Authorization': 'Token ' + key}

    try:
        response = requests.get(MINDAT_API_URL + "/geomaterials/", params=params, headers=headers)
        while response.status_code == 200 and is_valid_json(response):
            response_data = response.json()
            result_data = response_data.get("results", [])
            all_results.extend(result_data)

            next_url = response_data.get("next")
            if not next_url:
                break
            response = requests.get(next_url, headers=headers)
    except requests.RequestException as e:
        st.error(f"Request failed for {mineral}: {e}")

    if all_results:
        filtered_results = []
        # Filter the results to include only the selected fields
        for result in all_results:
            filtered_result = {mapped_fields_results_all[field] : result.get(field) for field in api_fields}
            filtered_results.append(filtered_result)

        # Write results to a temporary JSON file
        json_data = json.dumps(filtered_results, indent=4)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmpfile:
            tmpfile.write(json_data.encode('utf-8'))
            json_path = tmpfile.name

else:
    st.write("")

########################## modify and display results ################################################################

if all_results: 
    df = pd.DataFrame.from_dict(pd.json_normalize(filtered_results), orient='columns')
    new_formulas=[]
    mindat_links=[]
    corrected_ids=[]
    for formula in df["Formula (IMA)"]:
        new_formula=remove_sup_sub_tags(formula)
        new_formulas.append(new_formula)
    for id in df["ID"]:
        mindat_link='https://www.mindat.org/min-'+str(id)+'.html'
        mindat_links.append(mindat_link)
        corrected_id=str(id)
        corrected_ids.append(corrected_id)
    
    df["Formula (IMA)"]=new_formulas
    df["ID"]=corrected_ids
    if show_link==True:
        df["View Mineral on Mindat.org"]=mindat_links
    st.data_editor(
    df,
    column_config={
        "View Mineral on Mindat.org": st.column_config.LinkColumn("View Mineral on Mindat.org")
    },
    hide_index=True,
    )


 

############################################# download results ################################################################
    st.divider()
    st.subheader(subheader_5)
    st.write(info_2)
    st.download_button(
        label=label_button_2, use_container_width=True,
        data=json.dumps(filtered_results, indent=4),
        file_name='mineral_data.json',
        mime='application/json'
    )
 