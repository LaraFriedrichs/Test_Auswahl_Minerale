import streamlit as st
import requests

MINDAT_API_URL = "https://api.mindat.org"
key=st.secrets["api_key"]
field_str='name,id,type_localities'
headers = {'Authorization': 'Token ' + key}
params = {'format': 'json','fields':field_str}
all_results = []

def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False
if st.button('request ids'):
    try:
        response = requests.get(MINDAT_API_URL + "/minerals_ima/", params=params, headers=headers)
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
            st.error("Failed to fetch data")
            #st.error(f"Response content: {response.text}")
    except requests.RequestException as e:
        st.error("Request failed")
    all_results

############# Get the localities for  the important minerals########

params={'format','json'}
id=100
try:
    response = requests.get(MINDAT_API_URL + f"/localities/{id}/", params=params, headers=headers)
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
        st.error("Failed to fetch data")
        #st.error(f"Response content: {response.text}")
except requests.RequestException as e:
    st.error("Request failed")
all_results


#"latitude": 0.1,
#"longitude": 0.1,
# https://api.mindat.org/localities/{id}/