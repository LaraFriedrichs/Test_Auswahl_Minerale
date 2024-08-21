import streamlit as st

header = 'An Overview of the Most Important Minerals'
st.set_page_config(
    page_title= header,
    page_icon=':rock:',
)
st.sidebar.success("Select a page.")

# text and information 


subheader_1='Welcome!👋'
subheader_2='Select the mineral and the information you want to get'
subheader_3='Request the Information'
subheader_4='Results:'
subheader_5='Download Results'
info_1 =('This app can be used to get information about the most important minerals in geoscience. '
        'The information provided here is requested from mindat.org and only information for minerals '
        'which are approved by the International Mineralogical Association (IMA) are available. '
        'The shortcode and formula for the minerals are the IMA-shortcode and the IMA-formula. '
        'Your selected information will be requested from Mindat.org. If you want to explore more '
        'information about minerals, you can visit [Mindat.org](https://www.mindat.org).')
info_2 ='If you want, you can download the displayed results for the chosen mineral as a JSON file.'
label_selectbox_1='Which Mineral do you want to look at?'
label_selectbox_2='Select fields:'
label_button_1='Start requesting information!'
label_button_2='Download selected information as JSON'

# display Header and introduction
st.header(header)
st.divider()
st.subheader(subheader_1)
st.markdown(info_1)

