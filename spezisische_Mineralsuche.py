# imports
import streamlit as st
import requests
import json

# text and information 
header = 'An Overview of the Most Important Minerals'
introduction = 'This app can be used to get information about the most important minerals in geoscience. The information provided here is requested from mindat.org.'
info = 'The selected information for the important minerals is requested from Mindat.org. This process can take up to five minutes...'
label_selectbox='Which Information do you want to get?'
label_button='Start requesting Information!'
label_button_2='Download JSON'

# display Header and introduction
st.header(header)
st.markdown(introduction)
st.divider()

# Parameters API request
key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"

# select Information that schould be displayed
selection = st.multiselect(
    label=label_selectbox,
    options=['name', 'mindat_formula', 'ima_formula', 'description_short', 'elements', 'z', 'shortcode_ima']
)

# definition of the important minerals
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

# Function to check if the response is valid JSON
def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False
    
# Starting the request with a start button
if st.button(label=label_button, use_container_width=True):
    st.write(info)

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
            name = item.get("name", "Unnamed Mineral")
            with st.expander(name):
                for key, value in item.items():
                    if isinstance(value, list):
                        value = ', '.join(value)
                    st.write(f"**{key.capitalize()}:** {value}")

        # Display download button
        st.download_button(
            label=label_button_2,use_container_width=True,
            data=json_data,
            file_name='mineral_data.json',
            mime='application/json'
        )
    else:
        st.warning("No data retrieved.")
