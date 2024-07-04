import streamlit as st
import requests
import json
import pandas as pd

# Function to check if the response is valid JSON
def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

# text and information 
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
label_selectbox_1='Which Mineral do you want to look at?'
label_selectbox_2='Which information do you want to get?'
label_button_1='Start requesting information!'
label_button_2='Download selected information as JSON'

st.header('Get Information about a specific mineral')
st.markdown(info_1)
st.divider()
st.subheader(subheader_2)

# Parameters API request
key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"

# definition of the important minerals
url_data='https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/important_minerals.csv'
important_minerals = pd.read_csv(url_data)

# Mapping fields
list_all= ['Formula (IMA)','Shortcode (IMA)','About Name','Elements','Crystal System','Space Group Set','Polytype Of...','Morphology',
           'Twinning','Strunz Nomenclature Part 1','Strunz Nomenclature Part 2','Strunz Nomenclature Part 3','Strunz Nomenclature Part 4',
           'Weighting','Minimum Density','Maximum Density','Name']

fields_all = ['Formula (IMA)','Shortcode (IMA)','About Name','Elements','Crystal System','Space Group Set','Polytype Of...','Morphology',
    'Twinning','Strunz Nomenclature Part 1','Strunz Nomenclature Part 2','Strunz Nomenclature Part 3','Strunz Nomenclature Part 4','Weighting',
    'Minimum Density','Maximum Density','Name','ID','Long ID','GUID','Update Time','Mindat Formula','Mindat Formula Note','IMA Status','IMA Notes',
    'Variety Of','Syn ID','Group ID','Entry Type','Entry Type Text','Description Short','Impurities','Significant Elements','TL Form','CIM',
    'Occurrence','Other Occurrence','Industrial','Discovery Year','Diapheny','Cleavage','Parting','Tenacity','Colour','CS Metamict','Optical Extinction',
    'H Min','Hard Type','H Max','VHN Min','VHN Max','VHN Error','VHN G','VHN S','Luminescence','Lustre','Lustre Type','Other','Streak','Crystal Class',
    'Space Group','a','b','c','alpha','beta','gamma','a Error','b Error','c Error','Alpha Error','Beta Error','Gamma Error','va3','Z','D Measured',
    'D Measured 2','D Calculated','D Measured Error','D Calculated Error','Cleavage Type','Fracture Type','Epitaxi Description','Optical Type',
    'Optical Sign','Optical Alpha','Optical Beta','Optical Gamma','Optical Omega','Optical Epsilon','Optical Alpha 2','Optical Beta 2','Optical Gamma 2',
    'Optical Epsilon 2','Optical Omega 2','Optical N','Optical N 2','Optical 2V Calc','Optical 2V Measured','Optical 2V Calc 2','Optical 2V Measured 2',
    'Optical Alpha Error','Optical Beta Error','Optical Gamma Error','Optical Omega Error','Optical Epsilon Error','Optical N Error','Optical 2V Calc Error',
    'Optical 2V Measured Error','Optical Dispersion','Optical Pleochroism','Optical Pleochroism Description','Optical Birefringence','Optical Comments',
    'Optical Colour','Optical Internal','Optical Tropic','Optical Anisotropism','Optical Bireflectance','Optical R','UV','IR','Magnetism','Type Specimen Store',
    'Comment Hard','Dana 8th Edition Part 1','Dana 8th Edition Part 2','Dana 8th Edition Part 3','Dana 8th Edition Part 4','Thermal Behaviour','Comment Luster',
    'Comment Break','Comment Dense','Comment Crystal','Comment Color','Electrical','Tran Glide','No Loc Add','Spec Disp M','Approval Year','Publication Year',
    'IMA History','Rock Parent','Rock Parent 2','Rock Root','Rock BGS Code','Meteoritical Code','Key Elements','RIMIN','RIMAX']

    
field_mapping = {
    'Formula (IMA)': 'ima_formula',
    'Shortcode (IMA)': 'shortcode_ima',
    'About Name': 'aboutname',
    'Elements': 'elements',
    'Crystal System': 'csystem',
    'Space Group Set': 'spacegroupset',
    'Polytype Of...': 'polytypeof',
    'Morphology': 'morphology',
    'Twinning': 'twinning',
    'Strunz Nomenclature Part 1': 'strunz10ed1',
    'Strunz Nomenclature Part 2': 'strunz10ed2',
    'Strunz Nomenclature Part 3': 'strunz10ed3',
    'Strunz Nomenclature Part 4': 'strunz10ed4',
    'Weighting': 'weighting',
    'Minimum Density': 'dmeas',
    'Maximum Density': 'dmeas2', 
    'Name':'name',   
}

mapped_fields=list(field_mapping.keys())
mapped_fields_results = {v: k for k, v in field_mapping.items()}


field_mapping_all = {
    'ID': 'id',
    'Long ID': 'longid',
    'GUID': 'guid',
    'Name': 'name',
    'Update Time': 'updttime',
    'Mindat Formula': 'mindat_formula',
    'Mindat Formula Note': 'mindat_formula_note',
    'Formula (IMA)': 'ima_formula',
    'IMA Status': 'ima_status',
    'IMA Notes': 'ima_notes',
    'Variety Of': 'varietyof',
    'Syn ID': 'synid',
    'Polytype Of ...': 'polytypeof',
    'Group ID': 'groupid',
    'Entry Type': 'entrytype',
    'Entry Type Text': 'entrytype_text',
    'Description Short': 'description_short',
    'Impurities': 'impurities',
    'Elements': 'elements',
    'Significant Elements': 'sigelements',
    'TL Form': 'tlform',
    'CIM': 'cim',
    'Occurrence': 'occurrence',
    'Other Occurrence': 'otheroccurrence',
    'Industrial': 'industrial',
    'Discovery Year': 'discovery_year',
    'Diapheny': 'diapheny',
    'Cleavage': 'cleavage',
    'Parting': 'parting',
    'Tenacity': 'tenacity',
    'Colour': 'colour',
    'CS Metamict': 'csmetamict',
    'Optical Extinction': 'opticalextinction',
    'H Min': 'hmin',
    'Hard Type': 'hardtype',
    'H Max': 'hmax',
    'VHN Min': 'vhnmin',
    'VHN Max': 'vhnmax',
    'VHN Error': 'vhnerror',
    'VHN G': 'vhng',
    'VHN S': 'vhns',
    'Luminescence': 'luminescence',
    'Lustre': 'lustre',
    'Lustre Type': 'lustretype',
    'About Name': 'aboutname',
    'Other': 'other',
    'Streak': 'streak',
    'Crystal System': 'csystem',
    'Crystal Class': 'cclass',
    'Space Group': 'spacegroup',
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'alpha': 'alpha',
    'beta': 'beta',
    'gamma': 'gamma',
    'a Error': 'aerror',
    'b Error': 'berror',
    'c Error': 'cerror',
    'Alpha Error': 'alphaerror',
    'Beta Error': 'betaerror',
    'Gamma Error': 'gammaerror',
    'va3': 'va3',
    'Z': 'z',
    'Minimum Density': 'dmeas',
    'Maximum Density': 'dmeas2',
    'Density Calculated': 'dcalc',
    'Density Measured Error': 'dmeaserror',
    'Density Calculated Error': 'dcalcerror',
    'Cleavage Type': 'cleavagetype',
    'Fracture Type': 'fracturetype',
    'Morphology': 'morphology',
    'Twinning': 'twinning',
    'Epitaxi Description': 'epitaxidescription',
    'Optical Type': 'opticaltype',
    'Optical Sign': 'opticalsign',
    'Optical Alpha': 'opticalalpha',
    'Optical Beta': 'opticalbeta',
    'Optical Gamma': 'opticalgamma',
    'Optical Omega': 'opticalomega',
    'Optical Epsilon': 'opticalepsilon',
    'Optical Alpha 2': 'opticalalpha2',
    'Optical Beta 2': 'opticalbeta2',
    'Optical Gamma 2': 'opticalgamma2',
    'Optical Epsilon 2': 'opticalepsilon2',
    'Optical Omega 2': 'opticalomega2',
    'Optical N': 'opticaln',
    'Optical N 2': 'opticaln2',
    'Optical 2V Calc': 'optical2vcalc',
    'Optical 2V Measured': 'optical2vmeasured',
    'Optical 2V Calc 2': 'optical2vcalc2',
    'Optical 2V Measured 2': 'optical2vmeasured2',
    'Optical Alpha Error': 'opticalalphaerror',
    'Optical Beta Error': 'opticalbetaerror',
    'Optical Gamma Error': 'opticalgammaerror',
    'Optical Omega Error': 'opticalomegaerror',
    'Optical Epsilon Error': 'opticalepsilonerror',
    'Optical N Error': 'opticalnerror',
    'Optical 2V Calc Error': 'optical2vcalcerror',
    'Optical 2V Measured Error': 'optical2vmeasurederror',
    'Optical Dispersion': 'opticaldispersion',
    'Optical Pleochroism': 'opticalpleochroism',
    'Optical Pleochroism Description': 'opticalpleochorismdesc',
    'Optical Birefringence': 'opticalbirefringence',
    'Optical Comments': 'opticalcomments',
    'Optical Colour': 'opticalcolour',
    'Optical Internal': 'opticalinternal',
    'Optical Tropic': 'opticaltropic',
    'Optical Anisotropism': 'opticalanisotropism',
    'Optical Bireflectance': 'opticalbireflectance',
    'Optical R': 'opticalr',
    'UV': 'uv',
    'IR': 'ir',
    'Magnetism': 'magnetism',
    'Type Specimen Store': 'type_specimen_store',
    'Comment Hard': 'commenthard',
    'CIM': 'cim',
    'Strunz Nomenclature Part 1': 'strunz10ed1',
    'Strunz Nomenclature Part 2': 'strunz10ed2',
    'Strunz Nomenclature Part 3': 'strunz10ed3',
    'Strunz Nomenclature Part 4': 'strunz10ed4',
    'Dana 8th Edition Part 1': 'dana8ed1',
    'Dana 8th Edition Part 2': 'dana8ed2',
    'Dana 8th Edition Part 3': 'dana8ed3',
    'Dana 8th Edition Part 4': 'dana8ed4',
    'Thermal Behaviour': 'thermalbehaviour',
    'Comment Luster': 'commentluster',
    'Comment Break': 'commentbreak',
    'Comment Dense': 'commentdense',
    'Comment Crystal': 'commentcrystal',
    'Comment Color': 'commentcolor',
    'Electrical': 'electrical',
    'Tran Glide': 'tranglide',
    'No Loc Add': 'nolocadd',
    'Spec Disp M': 'specdispm',
    'Space Group Set': 'spacegroupset',
    'Approval Year': 'approval_year',
    'Publication Year': 'publication_year',
    'IMA History': 'ima_history',
    'Rock Parent': 'rock_parent',
    'Rock Parent 2': 'rock_parent2',
    'Rock Root': 'rock_root',
    'Rock BGS Code': 'rock_bgs_code',
    'Meteoritical Code': 'meteoritical_code',
    'Key Elements': 'key_elements',
    'Shortcode (IMA)': 'shortcode_ima',
    'RIMIN': 'rimin',
    'RIMAX': 'rimax',
    'Weighting': 'weighting',
}

mapped_fields_all=list(field_mapping_all.keys())
mapped_fields_results_all = {v: k for k, v in field_mapping_all.items()}

options_select=['Use Selection','Use all fields listed here','Use all fileds that are possible to request from Mindat.org/geomaterials']


# User Input

col1, col2 = st.columns(2)

# select Information that should be displayed
with col1:
    mineral = st.selectbox(label_selectbox_1, important_minerals)
    multiselect= st.multiselect(label=label_selectbox_2, options=mapped_fields)
# select mineral
with col2:
    radio_selection =st.radio('Select the Information you want to request:',options=options_select)
    start_request=st.button(label=label_button_1, use_container_width=True)

if radio_selection == 'Use all fields listed here':
    selection = list_all
    api_fields = [field_mapping[mapped_fields] for mapped_fields in selection]
    api_fields.insert(0,'name')
elif radio_selection == 'Use all fileds from Mindat.org/geomaterials':
    selection= fields_all
    api_fields = [field_mapping_all[mapped_fields] for mapped_fields in selection]
    api_fields.insert(0,'name')
elif radio_selection== 'Use Selection':
    selection = multiselect
    api_fields = [field_mapping[mapped_fields] for mapped_fields in selection]
    api_fields.insert(0,'name')
else:
    print('')

if start_request == True:
    st.divider()
    st.subheader(subheader_4)
    all_results = []
    params = {"name": mineral,"ima_status": "APPROVED", "format": "json"}
    headers = {'Authorization': 'Token ' + key}

    try:
        response = requests.get(MINDAT_API_URL + "/geomaterials/", params=params, headers=headers)
        if response.status_code == 200 and is_valid_json(response):
            result_data = response.json().get("results", [])
            all_results.extend(result_data)

            while response.json().get("next"):
                next_url = response.json()["next"]
                response = requests.get(next_url, headers=headers)
                if response.status_code == 200 and is_valid_json(response):
                    result_data = response.json().get("results", [])
                    all_results.extend(result_data)
                else:
                    break
        else:
            st.error(f"Failed to fetch data for {mineral}: {response.status_code}")
            st.error(f"Response content: {response.text}")
    except requests.RequestException as e:
        st.error(f"Request failed for {mineral}: {e}")

    if all_results:
        # Filter the results to include only the selected fields
        filtered_results = []

        for result in all_results:
             filtered_result = {mapped_fields_results_all[field]: result.get(field, None) for field in api_fields}
             filtered_results.append(filtered_result)

        # Write results to a JSON file
        json_data = json.dumps(filtered_results, indent=4)
        json_path = 'mineral_data.json'
        with open(json_path, 'w') as json_file:
            json_file.write(json_data)

        # Display results in dropdown format
        for item in filtered_results:
            name = item.get("Name")
            with st.expander(name,expanded=True):
                for key, value in item.items():
                    if isinstance(value, list):
                        value = ', '.join(value)
                    st.write(f"**{key.capitalize()}:** {value}")
 ####################################################
    # Display download button
    st.divider()
    st.subheader(subheader_5)
    st.write(info_2)
    st.download_button(
        label=label_button_2, use_container_width=True,
        data=json_data,
        file_name='mineral_data.json',
        mime='application/json'
    )
else:
    st.write("  ")