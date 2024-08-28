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

def filter_results(results, fields):
    filtered_results = []
    for result in results:
        filtered_result = {field: result.get(field) for field in fields}
        filtered_results.append(filtered_result)
    return filtered_results

################################################## API-Schlüssel und URL ##################################################

key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"

################################################# Text#########################################################################

st.header("Minerals and their Short Codes")
st.markdown("""
If you know the short code of a mineral and want to find out which mineral it belongs to, you can look up the mineral names here.
In addition, you will get some information about the minerals' names.
""")

################################################# Multiselect ###########################################################

url_1 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/shortcodes_important_minerals.csv"
shortcodes_important_minerals = pd.read_csv(url_1)

shortcode = st.selectbox("Enter a short code:", shortcodes_important_minerals)

################################################ API-Anfrage und Datenverarbeitung ########################################

st.spinner("Requesting data...")

params = {"shortcode_ima":shortcode,"ima_status": "APPROVED", "format": "json"}
headers = {'Authorization': 'Token'+ key}
api_fields = ["shortcode_ima", "name"]

# Daten von der API holen
all_results = fetch_mineral_data(MINDAT_API_URL + "/geomaterials/", params, headers)

# Daten filtern
if all_results:
    filtered_results=[]
    filtered_results = filter_results(all_results, api_fields)
    st.write("Filtered Results:", filtered_results)
    # Download-Button für JSON 
    st.download_button(
        label="Download results as JSON",
        data=json.dumps(filtered_results, indent=4),
        file_name='mineral_data.json',
        mime='application/json'
    )
else:
    st.write("No results found.")

