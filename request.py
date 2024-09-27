import os
import json
import requests
import pandas as pd

def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

# API-Schlüssel aus Umgebungsvariablen laden
key = os.getenv("MINDAT_API_KEY")
MINDAT_API_URL = "https://api.mindat.org"

if not key:
    raise ValueError("No API-Key found.")
    
important_minerals = ["Pyrope","Almandine",
"Spessartine","Grossular","Kyanite","Sillimanite","Andalusite","Gypsum","Baryte","Anhydrite","Pyrite","Chalcopyrite","Calcite","Aragonite","Dolomite","Ankerite","Siderite", 
"Magnesite", "Orthoclase","Albite","Sanidine","Microcline","Anorthite","Nepheline","Leucite","Sodalite","Nosean","Haüyne","Enstatite","Ferrosilite","Diopside",
"Hedenbergite","Jadeite","Omphacite","Kaolinite","Illite","Montmorillonite","Vermiculite","Phlogopite","Annite","Eastonite","Muscovite", "Phengite","Paragonite","Quartz",
"Rutile", "Hematite", "Ilmenite","Chromite","Magnetite","Tremolite","Actinolite","Glaucophane","Riebeckite","Lizardite","Augite","Chrysotile","Antigorite","Talc",
"Chlorite","Clinochlore","Chamosite","Tourmaline","Lawsonite","Epidote","Zoisite","Fayalite","Forsterite","Zircon","Titanite","Staurolite","Apatite","Monazite"]

all_results_stored = []

for mineral in important_minerals:

    params = {"name": mineral, "ima_status": "APPROVED", "format": "json"}
    headers = {'Authorization': 'Token ' + key}

    try:
        response = requests.get(MINDAT_API_URL + "/geomaterials/", params=params, headers=headers)
        while response.status_code == 200 and is_valid_json(response):
            response_data = response.json()
            result_data = response_data.get("results", [])
            all_results_stored.extend(result_data)

            next_url = response_data.get("next")
            if not next_url:
                break
            response = requests.get(next_url, headers=headers)
    except requests.RequestException as e:
        print(f"Request failed for {mineral}: {e}")

# Speichern als JSON-Datei im 'data'-Ordner
if all_results_stored:
    output_file_path = os.path.join('data', 'mineral_results.json')
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_results_stored, json_file, ensure_ascii=False, indent=4)
else:
    print("No results found.")
