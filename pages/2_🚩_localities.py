import streamlit as st
import pandas as pd
import requests
import json
import tempfile

# Function to check if the response is valid JSON
def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False
    
# Parameters API request

key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"
headers = {'Authorization': 'Token ' + key}
api_fields=['name','id','longid']

# definition of the important minerals
url_data='https://raw.githubusercontent.com/LaraFriedrichs/Test_Auswahl_Minerale/main/data/important_minerals.csv'
important_minerals = pd.read_csv(url_data)

st.header('Localities of the important minerals')
mineral= st.selectbox('Select a mineral', important_minerals)
params = {"name": mineral, "ima_status": "APPROVED", "format": "json"}
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
    st.error(f"Request failed for {mineral}: {e}")

if all_results:
        json_data = json.dumps(all_results, indent=4)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmpfile:
            tmpfile.write(json_data.encode('utf-8'))
            json_path = tmpfile.name
else:
    st.write("")

#for item in all_results:
    #st.write(item)


for entry in all_results:
    name = entry["name"]
    id = entry["id"]
    id_long = entry["longid"]

st.write("You choose "+str(name)+" the ID of "+str(name)+" is "+str(id)+".")
st.markdown("Check out the [Mindat.org page](f"https://www.mindat.org/min-{id}.html") for "+ str(name))

############# Get the localities for  the important minerals########
all_localities=[]
#try:
    #response = requests.get(MINDAT_API_URL + f"/localities/{id}/", params=params, headers=headers)
    #if response.status_code == 200 and is_valid_json(response):
        #result_data = response.json().get("results", [])
        #all_results.extend(result_data)

        #while response.json().get("next"):
            #next_url = response.json()["next"]
            #response = requests.get(next_url, headers=headers)
            #if response.status_code == 200 and is_valid_json(response):
                #result_data = response.json().get("results", [])
                #all_results.extend(result_data)
            #else:
                #break
    #else:
        #st.error("Failed to fetch data")
#except requests.RequestException as e:
    #st.error("Request failed")

#all_localities






#"latitude": 0.1,
#"longitude": 0.1,
# https://api.mindat.org/localities/{id}/