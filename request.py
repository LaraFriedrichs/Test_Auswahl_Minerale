import os
import json
import requests
import pandas as pd
import base64
import json
import requests


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
            all_results_stored.append(result_data)

            next_url = response_data.get("next")
            if not next_url:
                break
            response = requests.get(next_url, headers=headers)
    except requests.RequestException as e:
        print(f"Request failed for {mineral}: {e}")

# #####Lösung mit Github Acsess token ############

# GitHub API Informationen
repo = "LaraFriedrichs/Test_Auswahl_Minerale"  # Das Repository
path = "data/mineral_results.json"  # Pfad zur Datei im Repository
branch = "main"  # Branch, auf dem die Datei gespeichert wird
token = secrets.GITHUB_TOKEN # Dein GitHub Personal Access Token

# # Die Daten, die du speichern möchtest
data = all_results_stored

# # Konvertiere die Daten zu JSON
json_data = json.dumps(data, ensure_ascii=False, indent=4)

# # Base64-Kodierung der Daten (erforderlich für GitHub API)
encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

# URL für die API-Anfrage
url = f"https://api.github.com/repos/{repo}/contents/{path}"

# Prüfe, ob die Datei bereits existiert (um sie später zu aktualisieren)
response = requests.get(url, headers={"Authorization": f"token {token}"})
file_exists = response.status_code == 200

# Headers für die API-Anfrage
headers = {
    "Authorization": f"token {token}",
    "Content-Type": "application/json"
}

# API Body
if file_exists:
    # Wenn die Datei bereits existiert, brauchen wir den `sha`-Wert der bestehenden Datei, um sie zu aktualisieren
    sha = response.json()["sha"]
    message = "Update mineral_results.json"
    payload = {
        "message": message,
        "content": encoded_data,
        "sha": sha,
        "branch": branch
    }
else:
    # Wenn die Datei nicht existiert, erstellen wir eine neue
    message = "Add mineral_results.json"
    payload = {
        "message": message,
        "content": encoded_data,
        "branch": branch
    }

# POST oder PUT-Anfrage an die GitHub API
response = requests.put(url, headers=headers, data=json.dumps(payload))

# Überprüfung der Antwort
if response.status_code in [200, 201]:
    print("Die Datei wurde erfolgreich hochgeladen oder aktualisiert!")
else:
    print(f"Fehler beim Hochladen der Datei: {response.status_code}")
    print(response.json())
