# imports
import streamlit as st
import requests
import json
import pandas as pd

# text and information 
header = 'An Overview of the Most Important Minerals'
subheader_1='Select the mineral and the information you want to get'
subheader_2='Results:'
introduction = ('This app can be used to get information about the most important minerals in geoscience. '
                'The information provided here is requested from mindat.org and only information for minerals '
                'which are approved by the International Mineralogical Association (IMA) are available. '
                'The shortcode and formula for the minerals are the IMA-shortcode and the IMA-formula. '
                'Your selected information will be requested from Mindat.org. If you want to explore more '
                'information about minerals, you can visit [Mindat.org](https://www.mindat.org).')
info = 'If you want, you can download the displayed results for the chosen mineral as a JSON file.'
label_selectbox='Which information do you want to get?'
label_button='Start requesting information!'
label_button_2='Download selected information as JSON'

# display Header and introduction
st.header(header)
st.divider()
st.subheader('Welcome!')
st.markdown(introduction)
st.divider()
st.subheader(subheader_1)

# Parameters API request
key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"

# definition of the important minerals
url_data='https://raw.githubusercontent.com/LaraFriedrichs/New_App_minerale/main/data/important_minerals.csv'
important_minerals = pd.read_csv(url_data)

# User Input
col1, col2 = st.columns(2)
# select mineral
with col1:
    mineral = st.selectbox('Which Mineral do you want to look at?', important_minerals)
# select Information that should be displayed
with col2:
    selection = st.multiselect(label=label_selectbox, options=['ima_formula','shortcode_ima','aboutname','elements','csystem','spacegroupset','polytypeof','morphology','twinning','strunz10ed1','strunz10ed2','strunz10ed3','strunz10ed4','weighting','dmeas','dmeas2','dcalc','type_localities','locality'])
    selection.append('name')

# Function to check if the response is valid JSON
def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False
    
st.divider()
# Starting the request with a start button
st.subheader('Request the Information')
if st.button(label=label_button, use_container_width=True):
    st.divider()
    st.subheader(subheader_2)

    all_results = []
    filter_dict = {"name": mineral, "ima_status": "APPROVED", "format": "json"}
    headers = {'Authorization': 'Token ' + key}
    params = filter_dict

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
            filtered_result = {field: result.get(field, None) for field in selection}
            filtered_results.append(filtered_result)

        # Write results to a JSON file
        json_data = json.dumps(filtered_results, indent=4)
        json_path = 'mineral_data.json'
        with open(json_path, 'w') as json_file:
            json_file.write(json_data)

        # Display results in dropdown format
        for item in filtered_results:
            name = item.get("name")
            with st.expander(name):
                for key, value in item.items():
                    if isinstance(value, list):
                        value = ', '.join(value)
                    st.write(f"**{key.capitalize()}:** {value}")

    # Display download button
    st.divider()
    st.subheader('Download Results')
    st.write(info)
    st.download_button(
        label=label_button_2, use_container_width=True,
        data=json_data,
        file_name='mineral_data.json',
        #mime='application/json'
    )
else:
    st.write("  ")
