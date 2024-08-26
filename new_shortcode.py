############################# packages ############################

import streamlit as st
import requests
import pandas as pd

############################### functions ###############################
def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

############################## text ######################################
short_codes=[]
all_results = []


st.header("Minerals and their Short Codes")
st.markdown("If you know the short code of a mineral and want to find out which mineral it belongs to, you can look up the mineral names here. In addition you will get some Information about the minerals names.")
st.multiselect(label="Select mineral short code:", options=short_codes)
st.subheader("Results")

############################# parameters API- Requests #######################

key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"
fields_str='name,shortcode_ima'  
api_fields=['name','shortcode_ima']
params = {"ima_status":"APPROVED","fields": fields_str,"format": "json"}
headers = {"Authorization": "Token " + key}


############################ Request #####################################
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
    st.write("Request failed for")
all_results

#try:
    #response = requests.get(MINDAT_API_URL + "/geomaterials/", params=params, headers=headers)
    #while response.status_code == 200 and is_valid_json(response):
        #response_data = response.json()
        #result_data = response_data.get("results", [])
        #all_results.extend(result_data)

        #next_url = response_data.get("next")
        #if not next_url:
            #break
        #response = requests.get(next_url, headers=headers)
#xcept requests.RequestException as e:
    #st.error(f"Request failed! {e}")

results=[]

for entry in all_results:
    name = entry["name"]
    short_code = entry["shortcode_ima"]
    results.append(short_code)

results