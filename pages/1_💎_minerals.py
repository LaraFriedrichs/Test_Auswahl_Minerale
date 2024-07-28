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
    formula = re.sub(r'</sub>', '', formula)
    # Replace <sup> and </sup> with nothing
    formula = re.sub(r'<sup>', '', formula)
    formula = re.sub(r'</sup>', '', formula)
    return formula

# # Example usage
# chemical_formula = "Al<sub>2</sub>OSiO<sub>4</sub>"
# clean_formula = remove_sup_sub_tags(chemical_formula)
# print(clean_formula)

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

url_1 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/important_minerals.csv"#st.secrets["url1"]
url_2 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/listshort.csv"#st.secrets["url2"]
url_3 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/listall.csv"#st.secrets["url3"]
url_4 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/fieldsshort.json"#st.secrets["url4"]
url_5 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/fieldsall.json"#st.secrets["url5"]

important_minerals = pd.read_csv(url_1)

list_all= pd.read_csv(url_2)

fields_all = pd.read_csv(url_3)

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

options_select=['Use your selected fields','Use all fields you can select here','Use all fields that are possible to request from Mindat.org/geomaterials']
radio_selection = st.radio('', options=options_select)

# check link 

show_link=st.checkbox('Show the Mindat.org links for the selected minerals')

st.divider()
st.subheader(subheader_4)

if radio_selection == 'Use all fields you can select here':
    selection = list_all
    api_fields = [field_mapping[mapped_fields] for mapped_fields in selection]
    api_fields.insert(0, 'name')
    api_fields.insert(1, 'id')
elif radio_selection == 'Use all fields that are possible to request from Mindat.org/geomaterials':
    selection = fields_all
    api_fields = [field_mapping_all[mapped_fields_all] for mapped_fields_all in selection]
    api_fields.insert(0, 'name')
    api_fields.insert(1, 'id')
elif radio_selection == 'Use your selected fields':
    selection = multiselect
    api_fields = [field_mapping[mapped_fields] for mapped_fields in selection]
    api_fields.insert(0, 'name')
    api_fields.insert(1, 'id')
else:
    st.write("Please select an option to proceed.")

############################################################ API Request ########################################################

all_minerals_results = []
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
            filtered_result = {mapped_fields_results_all[field]: result.get(field, None) for field in api_fields}
            filtered_results.append(filtered_result)

        # Write results to a temporary JSON file
        json_data = json.dumps(filtered_results, indent=4)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmpfile:
            tmpfile.write(json_data.encode('utf-8'))
            json_path = tmpfile.name

        all_minerals_results.append(filtered_results)
else:
    st.write("")

############################################## Display results ################################################################
    
if all_minerals_results: 
    df = pd.DataFrame.from_dict(pd.json_normalize(filtered_results), orient='columns')
    df
    if show_link == True:
        for mineral_results in all_minerals_results:
            for item in mineral_results:
                name = item.get("Name")
                id = item.get("ID")
                st.markdown(f"View {name} on [Mindat.org](https://www.mindat.org/min-{id}.html) !")
####################################################### Download Results ###################################################
    st.divider()
    st.subheader(subheader_5)
    st.write(info_2)
    combined_results = [item for sublist in all_minerals_results for item in sublist] 
    json_data_combined = json.dumps(combined_results, indent=4)
    st.download_button(
        label=label_button_2, use_container_width=True,
        data=json_data_combined,
        file_name='mineral_data.json',
        mime='application/json'
    )
