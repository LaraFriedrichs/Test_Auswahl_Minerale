#Functions to check if the response is valid JSON

def is_valid_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False

# function to make html more readable

def remove_sup_sub_tags(chemical_formula):
    # Replace <sub> with _ and </sub> with nothing
    formula = re.sub(r'<sub>', '_', chemical_formula)
    # Replace <sup> and </sup> with nothing
    formula = re.sub(r'<sub>(.*?)</sub>', r'_\1', chemical_formula)
    # Replace <sup>...</sup> with ^ 
    formula = re.sub(r'<sup>(.*?)</sup>', r'^\1', formula)
    # Replace &middot
    formula = formula.replace('&middot;', '·')
    return formula

def fetch_mineral_data(url, params, headers):
    all_results = []
    try:
        response = requests.get(url, params=params, headers=headers)
        while response.status_code == 200 and is_valid_json(response):
            response_data = response.json()
            all_results.extend(response_data.get("results", []))
            next_url = response_data.get("next")
            if not next_url:
                break
            response = requests.get(next_url, headers=headers)
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
    return all_results

def filter_results_by_shortcode(results, shortcode, fields):
    filtered_results = []
    for result in results:
        if result.get("shortcode_ima") == shortcode:
            filtered_result = {field: result.get(field) for field in fields}
            filtered_results.append(filtered_result)
    return filtered_results



