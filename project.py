"""
Shows the project code with all steps of data loading, processing,  exploratory data analysis and model training
"""
import streamlit as st


st.markdown("""
<head>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
            
<style>
body {
    background-color: #ffffff; 
    color: #212529; 
    font-weight: bold;
    
}
</style>
""", unsafe_allow_html=True)

st.title("Exploratory Data Analysis (EDA)")
st.components.v1.html(open('./pages/BeijingAirQualityAnalysis.html',
                      'r').read(), width=1000, height=1000, scrolling=True)
