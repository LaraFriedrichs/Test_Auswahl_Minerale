import streamlit as st
import requests

def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

short_codes=[]

st.header("Minerals and their Short Codes")
st.markdown("If you know the short code of a mineral and want to find out which mineral it belongs to, you can look up the mineral names here. In addition you will get some Information about the minerals names.")
st.multiselect(label="Select mineral short code:", options=short_codes)
st.subheader("Results")

key = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"


all_results = []
fields_str='name,shortcode_ima'
    
params = {"ima_status":"APPROVED","fields": fields_str,"format": "json"}
headers = {"Authorization": "Token " + key}

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
all_results


ey = st.secrets["api_key"]
MINDAT_API_URL = "https://api.mindat.org"
headers = {'Authorization': 'Token ' + key}
api_fields=['name','shortcode_ima']
params = {"ima_status": "APPROVED", "format": "json"}
all_results = []

#try:
    #response = requests.get(MINDAT_API_URL + "/geomaterials/", params=params, headers=headers)
    #while response.status_code == 200 and is_valid_json(response):
        #response_data = response.json()
        #result_data = response_data.get("results", [])
        #all_results.extend(result_data)

        #next_url = response_data.get("next")
        #if not next_url:
           # break
        #response = requests.get(next_url, headers=headers)
#except requests.RequestException as e:
    #st.error(f"Request failed! {e}")

#all_results

#results=[]

#for entry in all_results:
    #name = entry["name"]
    #short_code = entry["shortcode_ima"]
    #results.append(short_code)

#results


#####################


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

if all_results:
    filtered_results = []
    # Filter the results to include only the selected fields
    for result in all_results:
        filtered_result = {all_results[field] : result.get(field) for field in api_fields}
        filtered_results.append(filtered_result)


    
    df = pd.DataFrame.from_dict(pd.json_normalize(filtered_results), orient='columns')
        
    df
############################################# download results ################################################################
    st.divider()
    st.subheader(subheader_4)
    st.write(info_2)
    st.download_button(
        label=label_button, use_container_width=True,
        data=json.dumps(filtered_results, indent=4),
        file_name='mineral_data.json',
        mime='application/json')

