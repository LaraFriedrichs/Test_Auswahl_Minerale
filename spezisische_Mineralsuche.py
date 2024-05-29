import streamlit as st
import requests
import json
from pathlib import Path
import time

# Texte für die App
header = 'An Overview of the Most Important Minerals'
info = 'This app can be used to get information about the most important minerals in geoscience. The information provided here is requested from mindat.org.'

# Darstellung Texte in Streamlit
st.header(header)
st.markdown(info)
st.divider()

# Parameter für API request
key = st.secrets["api_key"]
WORKING_DIR = '/workspaces/Test_Auswahl_Minerale/.venv'
MINDAT_API_URL = "https://api.mindat.org"
important_minerals = [
    "Pyrope", "Almandine", "Spessartine", "Grossular", "Kyanite",
    "Sillimanite", "Andalusite", "Gypsum", "Baryte", "Anhydrite",
    "Pyrite", "Chalcopyrite", "Calcite", "Aragonite", "Dolomite",
    "Ankerite", "Siderite", "Magnesite", "Orthoclase", "Albite",
    "Sanidine", "Microcline", "Anorthite", "Nepheline", "Leucite",
    "Sodalite", "Nosean", "Haüyne", "Enstatite", "Ferrosilite",
    "Diopside", "Hedenbergite", "Jadeite", "Omphacite",
    "Kaolinite", "Illite", "Montmorillonite", "Vermiculite",
    "Phlogopite", "Annite", "Eastonite", "Muscovite", "Phengite",
    "Paragonite", "Quartz", "Rutile", "Hematite", "Ilmenite",
    "Chromite", "Magnetite", "Tremolite", "Actinolite", "Glaucophane",
    "Riebeckite", "Lizardite", "Augite", "Chrysotile", "Antigorite",
    "Talc", "Chlorite", "Clinochlore", "Chamosite", "Tourmaline",
    "Lawsonite", "Epidote", "Zoisite", "Olivine", "Zircon", "Titanite", "Staurolite", "Apatite", "Monazite"
]

filter_file_name = "mindat_items_filter.json"
filter_file_path = Path(WORKING_DIR, filter_file_name)

# Function to check if the response is valid JSON
def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

# Start button
if st.button(label='Start requesting Information!', use_container_width=True):
    st.write("The selected information is requested from Mindat.org for all IMA-approved minerals. This process can take a few minutes...")

    all_results = []

    for i, mineral in enumerate(important_minerals):
        filter_dict = {"name": mineral, 'format': 'json'}
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

        # To avoid rate limiting
        time.sleep(1)

    # Write all results to the file
    with open(filter_file_path, 'w') as f:
        json.dump({"results": all_results}, f, indent=4)

    st.success(f"Successfully saved {len(all_results)} entries to {filter_file_path}")

    # Optionally, display the data
    st.write(all_results)
