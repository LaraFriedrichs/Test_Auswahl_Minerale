import streamlit as st
import requests
import json
import pandas as pd

def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

################################################## API-Schlüssel und URL ##################################################

key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"

################################################# Text#########################################################################

st.header("Minerals and their Short Codes")
st.markdown("If you know the short code of a mineral and want to find out which mineral it belongs to, you can look up the mineral names here. In addition you will get some Information about the minerals names.")

################################################# Multiselect ###########################################################

url_1 = "https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/shortcodes_important_minerals.csv"

shortcodes_important_minerals = pd.read_csv(url_1)

shortcode=st.selectbox("Enter a short code:",shortcodes_important_minerals)

################################################ API-Anfrage und Datenverarbeitung ########################################

params = {"ima_status": "APPROVED", "format": "json"}
headers = {'Authorization': 'Token ' + key}

all_results = []
try:
    response = requests.get(MINDAT_API_URL + "/geomaterials/", params=params, headers=headers)
    while response.status_code == 200 and is_valid_json(response):
        response_data = response.json()
        result_data = response_data.get("results", [])
        all_results.append(result_data)
        next_url = response_data.get("next")
        if not next_url:
            break
        response = requests.get(next_url, headers=headers)
except requests.RequestException as e:
    st.error("Request failed")

# Debugging: Anzeigen der gesamten Ergebnisse, um sicherzustellen, dass Daten abgerufen wurden
st.write("All Results:", all_results)

# Download-Buttons für JSON und CSV
st.download_button(
    label="Download results as JSON",
    data=json.dumps(all_results, indent=4),
    file_name='mineral_data.json',
    mime='application/json'
    )

