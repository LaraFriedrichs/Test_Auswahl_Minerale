import streamlit as st
import pandas as pd
import requests
import json

from utils.func import is_valid_json
from utils.func import remove_sup_sub_tags
from utils.func import fetch_mineral_data
from utils.func import filter_results_by_shortcode



header = 'An Overview of the Most Important Minerals'
st.set_page_config(
    page_title= header,
    page_icon=':rock:',
)

# text and information 

subheader_1='Welcome!👋'
subheader_2='Select the mineral and the information you want to get'
subheader_3='Request the Information'
subheader_4='Results:'
subheader_5='Download Results'
info_1 =('This app can be used to get information about the most important minerals in geoscience. '
        'The information provided here is requested from Mindat.org and only information for minerals '
        'which are approved by the International Mineralogical Association (IMA) are available. '
        'If you want to explore more '
        'information about minerals, you can visit [Mindat.org](https://www.mindat.org).')
info_2 ='If you want, you can download the displayed results for the chosen mineral as a JSON file.'
label_selectbox_1='Which Mineral do you want to look at?'
label_selectbox_2='Select fields:'
label_button_1='Start requesting information!'
label_button_2='Download selected information as JSON'

# display Header and introduction
st.header(header)
st.divider()
st.subheader(subheader_1)
st.markdown(info_1)

tab1, tab2 = st.tabs(["💎 minerals", "🔎 short codes"])

with tab1:
    header = 'Get Information about a specific mineral'
    subheader_1='Select the mineral and the information you want to get:'
    subheader_2='Request the Information'
    subheader_3='Results:'
    subheader_4='Download Results as JSON:'
    info_1 =('Here you can select some of the most important minerals in Geosience and get some Information about them for Example their Formulas, Elemnts, Crystalsystems and more.' 
             'The shortcode and formula for the minerals are the IMA-shortcode and the IMA-formula. '
            'Your selected information will be requested from Mindat.org .')
    info_2 ='If you want, you can download the displayed results for the chosen mineral as a JSON file.'
    label_selectbox_1='Select minerals:'
    label_selectbox_2='Select fields:'
    label_ckeckbox='Show the Mindat.org links for the selected minerals'
    label_button='Download selected information as JSON'

    st.header(header)
    st.markdown(info_1)
    st.divider()
    st.subheader(subheader_1)

######################################################### Parameters API request ######################################################################

    key = st.secrets["api_key"]
    MINDAT_API_URL = "https://api.mindat.org"

######################################################### Important minerals and field mapping ###########################################################

    url_1 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/important_minerals.csv"
    url_2 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/fieldsshort.json"
    url_3 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/fieldsall.json"

    important_minerals = pd.read_csv(url_1)

    fields_short = requests.get(url_2)
    field_mapping = fields_short.json()

    fields_all = requests.get(url_3)
    field_mapping_all = fields_all.json()

    mapped_fields=list(field_mapping.keys())
    mapped_fields_results = {v: k for k, v in field_mapping.items()}

    mapped_fields_all=list(field_mapping_all.keys())
    mapped_fields_results_all = {v: k for k, v in field_mapping_all.items()}

########################################## User Input ##########################################################################

    col1, col2 = st.columns(2)

# select minerals
    with col1:
        minerals=st.multiselect(label_selectbox_1,important_minerals)

# select fields
    with col2:
        multiselect = st.multiselect(label=label_selectbox_2, options=mapped_fields)

    options_select=['Select fields manually','Select all','Use all fields from Mindat.org/geomaterials']
    radio_selection = st.radio('', options=options_select)

# checkbox link 

    show_link=st.checkbox(label_ckeckbox)

    st.spinner("Requesting data...")

    st.divider()
    st.subheader(subheader_3)

    if radio_selection == 'Select all':
        selection = field_mapping  
        api_fields = [field_mapping.get(field) for field in selection]
        api_fields.insert(0, 'name')
        api_fields.insert(1, 'id')
        api_fields.insert(2, 'ima_formula')
    elif radio_selection == 'Use all fields from Mindat.org/geomaterials':
        selection = field_mapping_all  
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
        if radio_selection=='Use all fields from Mindat.org/geomaterials':
            new_formulas=[]
            for formula in df["Mindat Formula"]:
                new_formula=remove_sup_sub_tags(formula)
                new_formulas.append(new_formula)
            df["Mindat Formula"]=new_formulas

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
        st.subheader(subheader_4)
        st.write(info_2)
        st.download_button(
            label=label_button, use_container_width=True,
            data=json.dumps(filtered_results, indent=4),
            file_name='mineral_data.json',
            mime='application/json'
        )
  
with tab2:
    key = st.secrets["api_key"]
    MINDAT_API_URL = "https://api.mindat.org"

################################################# Text ####################################################################

    st.header("Minerals and their Short Codes")
    st.markdown("""Here you can look up some of the most important minerals in Geosience by using their shortcode.
        The information provided here is requested from mindat.org and only information for minerals 
        which are approved by the International Mineralogical Association (IMA) are available.
        The shortcode is the IMA-shortcode. Your selected information will be requested from Mindat.org. If you want to explore more 
        information about minerals, you can visit [Mindat.org](https://www.mindat.org).""")

################################################# Multiselect ###########################################################

    url_1 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/shortcodes_important_minerals.csv"
    shortcodes_important_minerals = pd.read_csv(url_1)
    st.divider()
    st.subheader("Enter a shortcode:")

    shortcodes = st.multiselect("", shortcodes_important_minerals)

################################################ API-Anfrage und Datenverarbeitung ########################################
    all_results=[]
    filtered_results=[]
    if shortcodes:
        with st.spinner("Requesting data..."):

            params = {"ima_status": "APPROVED", "format": "json"}
            headers = {'Authorization': f'Token {key}'}
            api_fields = ["shortcode_ima", "name", "aboutname"]

        # Daten von der API holen
            all_results = fetch_mineral_data(MINDAT_API_URL + "/geomaterials/", params, headers)
        
        # Ergebnisse nach den ausgewählten Shortcodes filtern
            for shortcode in shortcodes:
                filtered_result = filter_results_by_shortcode(all_results, shortcode, api_fields)
                if filtered_result:  # Überprüfen, ob Ergebnisse gefunden wurden
                    filtered_results.extend(filtered_result)

                # Ergebnisse anzeigen
                    for result in filtered_result:
                        with st.expander(shortcode, expanded=True,icon=None):
                            col1, col2 = st.columns(2)
                            col1.write(f"**Shortcode:** {result['shortcode_ima']}")
                            col2.write(f"**Name:** {result['name']}")
                            st.write(result['aboutname'])
                    # Download-Buttons für JSON
                    
                else:
                    st.write(f"No results found for shortcode '{shortcode}'.")
    else:
        st.write("Please select at least one shortcode.")
    if filtered_results:
        st.divider()
        st.subheader("Download Results as JSON:")
        st.write("If you want, you can download the results as a JSON file.")
        st.download_button(
                label="Download results as JSON",
                data=json.dumps(filtered_results, indent=4),
                file_name='mineral_data.json',
                mime='application/json'
                )

