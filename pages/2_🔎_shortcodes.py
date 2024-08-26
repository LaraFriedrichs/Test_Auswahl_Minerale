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
field_str='name,shortcode_ima'
params = {"ima_status":"APPROVED","fields": field_str,"format": "json"}
headers = {"Authorization": "Token " + key}


################################################# UI-Komponenten ###########################################################

st.header("Minerals and their Short Codes")
st.markdown("If you know the short code of a mineral and want to find out which mineral it belongs to, you can look up the mineral names here. In addition you will get some Information about the minerals names.")
st.subheader("Results")

################################################ API-Anfrage und Datenverarbeitung ########################################
all_results = []
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
    st.error("Request failed")
all_results

# Debugging: Anzeigen der gesamten Ergebnisse, um sicherzustellen, dass Daten abgerufen wurden
st.write("All Results:", all_results)

# Wenn Ergebnisse vorhanden sind, filtere sie und erstelle DataFrame
if all_results:
    # Extrahiere die Shortcodes und Namen
    short_codes = [entry["shortcode_ima"] for entry in all_results]
    selected_codes = st.multiselect("Select mineral short code:", options=short_codes)

    # Filtere die Ergebnisse basierend auf den ausgewählten Shortcodes
    filtered_results = [entry for entry in all_results if entry["shortcode_ima"] in selected_codes]

    # Debugging: Überprüfen, ob gefilterte Ergebnisse vorhanden sind
    st.write("Filtered Results:", filtered_results)

    # Zeige die gefilterten Ergebnisse an, falls welche vorhanden sind
    if filtered_results:
        df = pd.DataFrame(filtered_results)
        st.write(df)
        
        # Download-Buttons für JSON und CSV
        st.download_button(
            label="Download results as JSON",
            data=json.dumps(filtered_results, indent=4),
            file_name='mineral_data.json',
            mime='application/json'
        )

        st.download_button(
            label="Download results as CSV",
            data=df.to_csv(index=False),
            file_name='mineral_data.csv',
            mime='text/csv'
        )
    else:
        st.write("No results match your selection.")
else:
    st.write("No results found.")
