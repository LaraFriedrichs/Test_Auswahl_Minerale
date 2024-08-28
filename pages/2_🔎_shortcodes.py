import streamlit as st
import requests
import json
import pandas as pd

################################################## Funktionen ##################################################

@st.cache_data
def fetch_mineral_data(url, params, headers):
    all_results = []
    try:
        response = requests.get(url, params=params, headers=headers)
        while response.status_code == 200 and is_valid_json(response):
            response_data = response.json()
            all_results.extend(response_data.get("results", []))
            next_url = response_data.get("next")
            if not next_url:
                break
            response = requests.get(next_url, headers=headers)
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
    return all_results

def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

def filter_results_by_shortcode(results, shortcode, fields):
    filtered_results = []
    for result in results:
        if result.get("shortcode_ima") == shortcode:
            filtered_result = {field: result.get(field) for field in fields}
            filtered_results.append(filtered_result)
    return filtered_results

################################################## API-Schlüssel und URL ##################################################

key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"

################################################# Text#########################################################################

st.header("Minerals and their Short Codes")
st.markdown("""Here you can look up some of the most important minerals in Geosience by using their shortcode.
        The information provided here is requested from mindat.org and only information for minerals 
        which are approved by the International Mineralogical Association (IMA) are available.
        The shortcode is the IMA-shortcode. Your selected information will be requested from Mindat.org. If you want to explore more 
        information about minerals, you can visit [Mindat.org](https://www.mindat.org).""")

################################################# Selectbox ###########################################################

url_1 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/shortcodes_important_minerals.csv"
shortcodes_important_minerals = pd.read_csv(url_1)
st.divider()
st.subheader("Enter a shortcode:")

shortcodes = st.multiselect("", shortcodes_important_minerals)

################################################ API-Anfrage und Datenverarbeitung ########################################

with st.spinner("Requesting data..."):

    params = {"ima_status": "APPROVED", "format": "json"}
    headers = {'Authorization': f'Token {key}'}
    api_fields = ["shortcode_ima", "name","aboutname"]

    # Daten von der API holen
    all_results = fetch_mineral_data(MINDAT_API_URL + "/geomaterials/", params, headers)
    filtered_results=[]
    # Ergebnisse nach dem ausgewählten Shortcode filtern
    for shortcode in shortcodes:
        filtered_result = filter_results_by_shortcode(all_results, shortcode, api_fields)
        filtered_results.append(filtered_result)

        # Ergebnis anzeigen
        st.divider()
        st.subheader("Result:")
        if filtered_results:
            for result in filtered_results:
                col1, col2 = st.columns(2)
                col1.write(f"**Shortcode:** {result['shortcode_ima']}")
                col2.write(f"**Name:** {result['name']}")
                st.write(result['aboutname'])
        else:
            st.write(f"No results found.")

# Download-Buttons für JSON 
st.divider()
st.subheader("Downlaod Results as JSON:")
st.write("If you want you can download the results as a JSON - file.")
st.download_button(
    label="Download results as JSON",
    data=json.dumps(filtered_results, indent=4),
    file_name='mineral_data.json',
    mime='application/json'
)

