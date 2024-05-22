import streamlit as st
import requests
import json

st.header('An Overview of the Most Important Minerals')
st.divider()
st.markdown('This app can be used to get information about the most important minerals in geoscience. The information provided here is requested from mindat.org.')
st.divider()

selected_fields = st.multiselect(label="Which information do you want to get?", options=['name', 'mindat_formula', 'ima_formula', 'description_short','elements','z','shortcode_ima'])
fields_str = ",".join(selected_fields)


if st.button(label='Start requesting Information!', use_container_width=True):
    st.write("The selected information is requested from Mindat.org for all IMA-approved minerals. This process can take a few minutes...")
    key = st.secrets["api_key"]
    #Pyrope="Pyrope"
    #Almandine="Almandine"
    #Spessartine="Spessartine"
    MINDAT_API_URL = "https://api.mindat.org"
    important_minerals = ["Pyrope","Almandine","Spessartine", "Grossular", "Kyanite",
        "Sillimanite", "Andalusite", "Gypsum", "Baryte", "Anhydryte",
        "Pyrite", "Chalcopyrite", "Calcite", "Aragonite", "Dolomite",
        "Ankerite", "Siderite", "Magnesite", "Orthoclase", "Albite",
        "Sanidine", "Microcline", "Anorthite", "Nepheline", "Leucite",
        "Sodalite", "Nosean", "Haüyne", "Enstatite", "Ferrosilite",
        "Diopside", "Hedenbergite", "Jadeite", "Omphacite",
        "Kaolinite", "Illite", "Montmorillonite", "Vermiculite",
        "Phlogopite", "Annite", "Eastonite", "Muscovite", "Phengite",
        "Paragonite", "Quartz", "Rutile", "Hematite", "Ilmenite",
        "Chromite", "Magnetite", "Tremolite", "Actinolite", "Glaucophane",
        "Riebeckite", "Lizadrdite", "Augite", "Chrysotile", "Antigorite",
        "Talc", "Chlorite", "Clinochlor", "Chamosite", "Tourmaline",
        "Lawsonite", "Epidote", "Zoisite", "Olivine", "Zircon", "Titanite", "Staurolite", "Apatite", "Monazite"]
    for i in range(1,len(important_minerals)):
        headers = {'Authorization': 'Token ' + key}
        filter_dict={"name":str(important_minerals[i])}
        params_2={'fields': fields_str,'format': 'json'}
        params=filter_dict
    
        response = requests.get(MINDAT_API_URL + "/geomaterials/", params=params, headers=headers)
        if response.status_code != 200:
            st.error("Failed to fetch data from the API.")
        else:
            json_data = {"results": response.json().get("results", [])}
        
            while response.json().get("next"):
                next_url = response.json()["next"]
                response = requests.get(next_url, headers=headers)
                if response.status_code == 200:
                    json_data["results"] += response.json().get("results", [])
                else:
                    break
        
            #st.session_state.json_data = json_data
            with open('minerals_data.json', 'w') as json_file:
                json.dump(json_data, json_file)
            st.write(json_data)   
