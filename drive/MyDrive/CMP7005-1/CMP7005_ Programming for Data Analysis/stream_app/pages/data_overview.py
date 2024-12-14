import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)

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

data = pd.read_csv('data/merged_data.csv')


st.markdown("""
<style>
      th {
            width: 200px;
            font-weight: bold;
            font-size: 20px;
            color: #0d6efd;
        }

        th,
        td {
            text-align: center;
        }

        table {
            margin: 0 auto;
            width: 80%;
        }
        
</style>
""", unsafe_allow_html=True)

st.markdown("""<h2 class="text-center text-primary mb-4">Beijing Air Quality Dataset Overview</h2>""", unsafe_allow_html=True)

st.subheader('Sample 10 Records:')
html_sample_data = data.sample(10).to_html(classes='table table-striped', index=False)
st.markdown(html_sample_data, unsafe_allow_html=True)


st.subheader('Summary Statistics:')
html_data_summary = data.describe().T.to_html(classes='table table-striped', index=False)
st.markdown(html_data_summary, unsafe_allow_html=True)



st.subheader('Missing Data and Variable Information:')
missing_data = data.isnull().sum()
missing_data_percentage = (data.isnull().sum() / len(data)) * 100
missing_data_info = pd.DataFrame({
    'Missing Values': missing_data,
    'Percentage': missing_data_percentage,
    'Data Type': data.dtypes
}).reset_index()
missing_data_info.columns = ['Column Name',
                             'Missing Values', 'Percentage', 'Data Type']

html_missing_data_info = missing_data_info.to_html(
    classes='table table-striped', index=False)
st.markdown(
    html_missing_data_info,
    unsafe_allow_html=True
)


df_num = data.select_dtypes(include=["float", "int"]).drop(
    columns=["year", "month", "day", "hour"])

# Correlation heatmap
st.subheader("Correlation Among Pollutant Related Features")
plt.figure(figsize=(20, 20))
corr = df_num.corr()
sns.heatmap(corr, annot=True, cmap="YlGnBu", cbar=False)
plt.title("Correlation Among Pollutant Related Features",
          fontsize=16, fontweight='bold')
plt.xticks(rotation=45, fontweight='bold')
plt.yticks(rotation=45, fontweight='bold')
st.pyplot()

st.markdown("""
### Observation from Correlation Analysis

- **PM2.5** and **PM10** are strongly correlated, and their levels are linked with common sources of pollution, such as industrial emissions and vehicular traffic.
- **CO**, **NO2**, and **SO2** tend to increase together, reflecting emissions from combustion processes.
- **Ozone (O3)** behaves differently, showing negative correlations with most primary pollutants, especially NO2.
- **Temperature** and **dew point** have a strong relationship, and both can influence pollutant behavior, with higher temperatures generally leading to lower concentrations of particulate matter.
- **Rainfall** and **wind speed** show weak to moderate impacts on air quality, with wind likely dispersing pollutants and rainfall having a temporary cleansing effect.
""")

# Top correlations with PM2.5
pm25_corr = corr['PM2.5'].abs().sort_values(ascending=False)
top_corr = pm25_corr.index[1:]  # Exclude PM2.5 itself

st.subheader("Top Correlations with PM2.5")
plt.figure(figsize=(14, 8))
sns.barplot(x=pm25_corr[top_corr], y=top_corr, palette='rocket')
plt.title('Top Correlations with PM2.5', fontsize=16, fontweight='bold')
plt.xlabel('Absolute Correlation', fontsize=12)
plt.ylabel('Features', fontsize=12)
st.pyplot()

st.markdown("""
### Observation from Top Correlations with PM2.5

- **PM2.5** shows strong positive correlations with **PM10** (0.88), **CO** (0.77), and **NO2** (0.66), indicating that these pollutants often rise together, likely due to shared sources like traffic and industrial emissions.
- It has moderate correlation with **SO2** (0.48).
- The correlation with **wind speed** (0.27) is weak, suggesting that wind has a limited effect on PM2.5 concentrations.
- There’s a weak positive correlation with **O3** (0.15), likely due to overlapping conditions affecting both pollutants, and a very weak correlation with **temperature** (0.13), indicating that temperature has little direct impact on PM2.5 levels.
- The correlations with **dew point** (0.11), **pressure** (0.02), and **rain** (0.01) are very weak, showing minimal influence on PM2.5 concentrations.
""")
