import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

# Global Matplotlib configurations
plt.rcParams.update({
    'figure.figsize': (20, 16),
    'axes.labelsize': 16,
    'axes.labelweight': 'bold',
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'lines.linewidth': 2,
})

# lets just use a sample..
data = pd.read_csv('data/merged_data.csv').sample(50000)

data.drop(columns = ["No"], inplace=True)
data["wd"]  = data["wd"].fillna(method='ffill')
data[data.select_dtypes(exclude=["object"]).columns] = data.select_dtypes(exclude=["object"]).fillna(data.select_dtypes(exclude=["object"]).mean())
data['datetime'] = pd.to_datetime(data[['year', 'month', 'day']])

# Function to plot data distribution
def plot_data_distribution(data, category='AIR'):
    """
    Parameters:
    - data (pd.DataFrame)
    - category (str): either ('AIR' or 'WEATHER'). 
                      'AIR' plots air quality components, 
                      'WEATHER' plots weather-related parameters (e.g., precipitation, temperature).
    """
    if category == 'AIR':
        variables = ['NO2', 'O3', 'SO2']
        category_title = "Air Quality Components"
        super_title = "Distribution and Boxplots of Key Air Quality Components (NO2, O3, SO2)"
    elif category == 'WEATHER':
        variables = ['TEMP', 'PRES', 'RAIN']
        category_title = "Weather Parameters"
        super_title = "Distribution and Boxplots of Key Weather Parameters (Temperature, Pressure, Precipitation)"
    else:
        raise ValueError("Invalid category. Choose either 'AIR' or 'WEATHER'.")

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    for i, feature in enumerate(variables):
        row = i // 3
        col = i % 3

        sns.histplot(data[feature], kde=True, bins=20,
                     color='skyblue', ax=axes[row, col])
        axes[row, col].set_title(
            f'Distribution of {feature} ({category_title})', fontsize=14, fontweight='bold')
        axes[row, col].set_xlabel(feature)
        axes[row, col].set_ylabel('Frequency')
        sns.boxplot(data[feature], orient='h', ax=axes[row +
                    1, col] if row+1 < 2 else axes[row, col])
        axes[row+1, col].set_title(
            f'Boxplot of {feature} ({category_title})', fontsize=14, fontweight='bold')
        axes[row+1, col].set_xlabel(feature)
    plt.suptitle(super_title, fontsize=18,
                 fontweight='bold', ha='center', y=1.02)
    plt.tight_layout()
    st.pyplot()


st.title("Data Analysis and Visualizations")


st.subheader("Air Quality Distribution by Air Pollutants")
plot_data_distribution(data, category='AIR')

st.subheader("Weather Distribution by Weather Parameters")
plot_data_distribution(data, category='WEATHER')

# results for above
st.markdown("""
### Observation
- Interms of distribution, the following can be observed for each case;
    - The distribution of `temperature` likely shows a bimodal which is also near-normal distribution. This is becuase of different seasonal variation in Beijing where the peak are the warmer periods. As from the box plot, it can be observed that the distribution is centered around the mean with no outliers. It's mean is aound 14 degrees
    - The `pressure` distribution is **near symmetric**, with small change around a mean value. There are no outlier identified and its mean is around 1010.
    - The rainfall distribution is **very rightly-skewed**, with most data points showing little or no rainfall and a smaller number of days with heavy rainfall. This hence cause it to show multiple outliers due to large deviation in values.
    - The distribution of `NO2` is **right-skewed**, showing higher concentrations during winter months due to traffic and heating, and lower levels during warmer months. It has fewer outliers which might be due to instances of heavy pollution events.
    - The `O3/Ozone` distribution has a **rightly skewed**, and has a very large variation hence more outliers.
    - `SO2` is **right-skewed**, with a majority of days showing low concentrations, but some outliers indicating pollution spikes, often linked to industrial activities or certain weather conditions.
                    
""")

# create split and multiple lines
st.subheader("EDA on Pollutants and Weather Parameters")

st.markdown(
    """---
    """
)
st.markdown("""<br><br>""", unsafe_allow_html=True)
# optionals for others.
optional_eda = st.selectbox(
    "Select Additional Pollutant  and Weather Analysis", [
        "Line Plot for Monthly Pollutants Monthly Trends",
        "Line plot and Boxplot for Hourly Trends Weather and Air",
        "Pollutant Heatmap for Hourly and Monthly Trends",
        "Correlation Anlysis of DEw Point vs. Air Quality",
        "Correlation Anlysis of Wind Speed (WSPM) and Direction (wd) vs. Air Quality",
        "Correlation Anlysis of Temperature (TEMP) vs. Air Quality"
    ])


if optional_eda == "Line Plot for Monthly Pollutants Monthly Trends":
    st.subheader("Line Plot for Monthly Pollutants Monthly Trends")
    st.write("Explore the monthly trends for PM2.5, NO2, O3, SO2, and CO.")

    st.subheader("Monthly Average Pollutant Concentration")
    data['year_month'] = data['year'].astype(
        str) + '-' + data['month'].astype(str).str.zfill(2)
    # Plot PM2.5 trend
    plt.subplot(5, 1, 1)
    monthly_pm25 = data.groupby('year_month')['PM2.5'].mean()
    monthly_pm25.plot(kind='line', color='skyblue', marker='o')
    plt.title('Monthly Average PM2.5 Concentration',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('PM2.5 (µg/m³)', fontsize=12)

    # Plot NO2 trend
    plt.subplot(5, 1, 2)
    monthly_no2 = data.groupby('year_month')['NO2'].mean()
    monthly_no2.plot(kind='line', color='lightgreen', marker='o')
    plt.title('Monthly Average NO2 Concentration',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('NO2 (µg/m³)', fontsize=12)

    # Plot O3 trend
    plt.subplot(5, 1, 3)
    monthly_o3 = data.groupby('year_month')['O3'].mean()
    monthly_o3.plot(kind='line', color='lightcoral', marker='o')
    plt.title('Monthly Average O3 Concentration',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('O3 (µg/m³)', fontsize=12)

    # Plot SO2 trend
    plt.subplot(5, 1, 4)
    monthly_so2 = data.groupby('year_month')['SO2'].mean()
    monthly_so2.plot(kind='line', color='red', marker='o')
    plt.title('Monthly Average SO2 Concentration',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('SO2 (µg/m³)', fontsize=12)

    # Plot CO trend
    plt.subplot(5, 1, 5)
    monthly_co = data.groupby('year_month')['CO'].mean()
    monthly_co.plot(kind='line', color='purple', marker='o')
    plt.title('Monthly Average CO Concentration',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('CO (µg/m³)', fontsize=12)

    plt.tight_layout()
    st.pyplot()

    # Observations for Monthly Trends
    st.markdown("""
    ### Observations for Monthly Trends:

    - **PM2.5, NO2, and SO2** concentrations show an increase during the colder months (November to February), likely due to heating and increased vehicle use during winter.
    - **Ozone (O3)** concentrations tend to peak during the warmer months (May to August), likely due to higher sunlight and temperature.
    - **CO** concentrations exhibit a similar trend to NO2, reflecting similar sources of pollution.
    - A noticeable inverse relationship between **PM2.5/NO2/SO2** and **O3** can be observed in certain months.
    """)

elif optional_eda == "Line plot and Boxplot for Hourly Trends Weather and Air":
    st.subheader("Line plot and Boxplot for Hourly Trends Weather and Air")
    st.write(
        "Explore the hourly trends for PM2.5, NO2, O3, SO2, CO, TEMP, PRES, DEWP, and WSPM.")

    # do the line plots
    columns = ["PM2.5", "PM10", "NO2", "O3",
               "SO2", 'TEMP', 'PRES', 'DEWP', "WSPM"]
    colors = sns.color_palette("Set2", n_colors=len(columns))
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 15))
    axes = axes.flatten()
    for i, column in enumerate(columns):
        data_hr = data[[column, 'hour']].groupby("hour").median(
        ).reset_index().sort_values(by='hour', ascending=False)

        sns.pointplot(x='hour', y=column, data=data_hr, markers='o',
                      color=colors[i % len(colors)], ax=axes[i])

        axes[i].set_title(
            f"Hourly Analysis for {column}", fontweight='bold', fontsize=14)
        axes[i].set_xlabel("Hour", fontweight='bold', fontsize=12)
        axes[i].set_ylabel(f"{column} Values", fontweight='bold', fontsize=12)

    plt.tight_layout()
    st.pyplot()

    plt.subplot(5, 1, 1)
    sns.boxplot(x='hour', y='PM2.5', data=data,
                palette='Blues', showfliers=False)
    plt.title('Hourly PM2.5 Concentration', fontsize=16, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('PM2.5 (µg/m³)', fontsize=12)

    plt.subplot(5, 1, 2)
    sns.boxplot(x='hour', y='NO2', data=data,
                palette='Greens', showfliers=False)
    plt.title('Hourly NO2 Concentration', fontsize=16, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('NO2 (µg/m³)', fontsize=12)

    plt.subplot(5, 1, 3)
    sns.boxplot(x='hour', y='O3', data=data, palette='Reds', showfliers=False)
    plt.title('Hourly O3 Concentration', fontsize=16, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('O3 (µg/m³)', fontsize=12)

    plt.subplot(5, 1, 4)
    sns.boxplot(x='hour', y='SO2', data=data,
                palette='Purples', showfliers=False)
    plt.title('Hourly  SO2 Concentration', fontsize=16, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('SO2 (µg/m³)', fontsize=12)

    plt.subplot(5, 1, 5)
    sns.boxplot(x='hour', y='CO', data=data,
                palette='rocket', showfliers=False)
    plt.title('Hourly  CO Concentration', fontsize=16, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('CO (µg/m³)', fontsize=12)

    plt.tight_layout()
    st.pyplot()

    st.title("Observations on Hourly Pollution Levels")

    # Display the observations as markdown
    st.markdown("""
    ## Observations:

    - **PM2.5, CO, and NO2**: It is observed that there are higher pollution levels during peak hours, particularly between **7 AM to 9 AM** and **5 PM to 7 PM**. These spikes are likely associated with increased motor emissions during **morning and evening rush hours** when traffic congestion is at its highest.
    - **SO2**: The concentration of **SO2** tends to be elevated from **7 AM until about 6 PM**, which corresponds to typical **working hours**. This pattern suggests that SO2 levels are tied to industrial and combustion activities during regular workdays.
    - **PM2.5 Levels**: PM2.5 concentrations tend to be higher in the **early morning** and **evening**. These times coincide with peak traffic periods, likely contributing to higher pollution levels due to motor vehicle emissions.
    - **Ozone (O3)**: Ozone shows higher levels from **11 AM to 7 PM**, with a significant peak from **1 PM to 6 PM**. This is likely due to **sunlight** triggering the formation of ozone through reactions with **NO2 emissions**. As ozone is a photochemical pollutant, it tends to reach its highest levels on **sunny days**, particularly in the afternoon when sunlight is strongest.
    """)


elif optional_eda == 'Pollutant Heatmap for Hourly and Monthly Trends':
    st.subheader("Heatmap for Hourly and Monthly Trends")
    st.markdown(""" 
                In this heatmap is gonna be used to view summary of how pollutant levels (e.g., PM2.5, NO2, O3) vary across both the month and hour of the day. It helps to see if there are patterns influenced by both the time of the day or seasonal factors.
                """)

    # create pivottnfor data to get the average pollutant level per month and hour
    pm25_pivot = data.pivot_table(
        values='PM2.5', index='hour', columns='month', aggfunc=np.mean)
    no2_pivot = data.pivot_table(
        values='NO2', index='hour', columns='month', aggfunc=np.mean)
    o3_pivot = data.pivot_table(
        values='O3', index='hour', columns='month', aggfunc=np.mean)
    so2_pivot = data.pivot_table(
        values='SO2', index='hour', columns='month', aggfunc=np.mean)
    co_pivot = data.pivot_table(
        values='CO', index='hour', columns='month', aggfunc=np.mean)

    plt.figure(figsize=(18, 15))

    plt.subplot(5, 1, 1)
    sns.heatmap(pm25_pivot, cmap='Blues', annot=False,
                cbar_kws={'label': 'PM2.5 (µg/m³)'})
    plt.title('Heatmap of PM2.5 by Hour and Month',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Hour of the Day', fontsize=12)

    plt.subplot(5, 1, 2)
    sns.heatmap(no2_pivot, cmap='Greens', annot=False,
                cbar_kws={'label': 'NO2 (µg/m³)'})
    plt.title('Heatmap of NO2 by Hour and Month',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Hour of the Day', fontsize=12)

    plt.subplot(5, 1, 3)
    sns.heatmap(o3_pivot, cmap='Reds', annot=False,
                cbar_kws={'label': 'O3 (µg/m³)'})
    plt.title('Heatmap of O3 by Hour and Month',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Hour of the Day', fontsize=12)

    plt.subplot(5, 1, 4)
    sns.heatmap(so2_pivot, cmap='rocket_r', annot=False,
                cbar_kws={'label': 'SO2 (µg/m³)'})
    plt.title('Heatmap of SO2 by Hour and Month',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Hour of the Day', fontsize=12)

    plt.subplot(5, 1, 5)
    sns.heatmap(co_pivot, cmap='mako_r', annot=False,
                cbar_kws={'label': 'CO (µg/m³)'})
    plt.title('Heatmap of CO by Hour and Month',
              fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Hour of the Day', fontsize=12)

    plt.tight_layout()
    st.pyplot()

    st.markdown("""
                ## Observations

            In the above analysis, it is observed that **PM2.5**, **CO**, and **NO2** heatmaps show higher pollutant levels during **winter months** (i.e., **December**, **January**, and **February**), as well as during **October** and **November**. These pollutants also peak during **rush hours** (i.e., **7-9 AM** and **5-7 PM**). This pattern is consistent with increased emissions from **heating** and **vehicle traffic** in colder months.

            For **Ozone (O3)**, the levels show a spike from **April to August** (the warmer months), with more concentration between **12 PM to 6 PM**. This could be sun-driven, as **Ozone (O3)** is formed through **photochemical reactions** in the presence of sunlight.

            For **SO2**, there is a noticeable higher concentration across **January**, **February**, **March**, **November**, and **December**. The trend for **SO2** shows that it is more concentrated during the colder months, suggesting that it could be related to **industrial** activities and **combustion** processes that occur more frequently in winter. It seems to be **inversely related to O3**.

            ### Summary:
            From the above three graphs, it can be summarized that:
            - **PM2.5**, **NO2**, **CO**, and **SO2** are likely to peak during **colder periods** and **rush hours**.
            - **Ozone (O3)** is more likely to peak during **warmer months**, especially around **midday (12 PM to 6 PM)**.
        """)


elif optional_eda == "Correlation Anlysis of Temperature (TEMP) vs. Air Quality":
    st.subheader("Correlation Analysis of Temperature (TEMP) vs. Air Quality")
    st.markdown("""Temperature can influence air pollutants concentrations , especially O3 (ozone), which forms under sunlight and higher temperatures.""")

    # Plot PM2.5 vs. Temperature
    plt.subplot(2, 2, 1)
    sns.scatterplot(x='TEMP', y='PM2.5', data=data, color='skyblue')
    plt.title('PM2.5 vs Temperature', fontsize=16, fontweight='bold')
    plt.xlabel('Temperature (°C)', fontsize=12)
    plt.ylabel('PM2.5 (µg/m³)', fontsize=12)

    # Plot NO2 vs. Temperature
    plt.subplot(2, 2, 2)
    sns.scatterplot(x='TEMP', y='NO2', data=data, color='lightgreen')
    plt.title('NO2 vs Temperature', fontsize=16, fontweight='bold')
    plt.xlabel('Temperature (°C)', fontsize=12)
    plt.ylabel('NO2 (µg/m³)', fontsize=12)

    # Plot O3 vs. Temperature
    plt.subplot(2, 2, 3)
    sns.scatterplot(x='TEMP', y='O3', data=data, color='lightcoral')
    plt.title('O3 vs Temperature', fontsize=16, fontweight='bold')
    plt.xlabel('Temperature (°C)', fontsize=12)
    plt.ylabel('O3 (µg/m³)', fontsize=12)

    # Plot SO2 vs. Temperature
    plt.subplot(2, 2, 4)
    sns.scatterplot(x='TEMP', y='SO2', data=data, color='yellow')
    plt.title('SO2 vs Temperature', fontsize=16, fontweight='bold')
    plt.xlabel('Temperature (°C)', fontsize=12)
    plt.ylabel('SO2 (µg/m³)', fontsize=12)

    plt.tight_layout()
    st.pyplot()
    st.markdown("""
        ### Observations:
        - For the case of `PM2.5, SO2 and NO2`, the temperature shows no direct correlation since these pollutants are more influenced by emissions (mostly engines/motor emissions), heating (in colder months), and weather patterns rather than temperature alone.
        - For the case of `O3(Ozone)`, it is seen that there appear some positive correlation between O3 and temperature because ozone is a secondary pollutant formed from reactions between NOx emissions and sunlight, which is more intense during warmer temperatures.
        """)


elif optional_eda == "Correlation Anlysis of Wind Speed (WSPM) and Direction (wd) vs. Air Quality":
    st.subheader(
        "Correlation Analysis of Wind Speed (WSPM) and Direction (wd) vs. Air Quality")
    st.markdown("""Wind speed and direction can influence air quality. Wind speed is measured in m/s, and direction is measured in degrees from 0° (north) clockwise. """)

    # Plot PM2.5 vs. Wind Speed
    plt.subplot(2, 2, 1)
    sns.scatterplot(x='WSPM', y='PM2.5', data=data, color='blue')
    plt.title('PM2.5 vs Wind Speed', fontsize=16, fontweight='bold')
    plt.xlabel('Wind Speed (m/s)', fontsize=12)
    plt.ylabel('PM2.5 (µg/m³)', fontsize=12)

    # Plot NO2 vs. Wind Speed
    plt.subplot(2, 2, 2)
    sns.scatterplot(x='WSPM', y='NO2', data=data, color='green')
    plt.title('NO2 vs Wind Speed', fontsize=16, fontweight='bold')
    plt.xlabel('Wind Speed (m/s)', fontsize=12)
    plt.ylabel('NO2 (µg/m³)', fontsize=12)

    # Plot O3 vs. Wind Speed
    plt.subplot(2, 2, 3)
    sns.scatterplot(x='WSPM', y='O3', data=data, color='red')
    plt.title('O3 vs Wind Speed', fontsize=16, fontweight='bold')
    plt.xlabel('Wind Speed (m/s)', fontsize=12)
    plt.ylabel('O3 (µg/m³)', fontsize=12)

    # Plot CO vs. Wind Speed
    plt.subplot(2, 2, 4)
    sns.scatterplot(x='WSPM', y='CO', data=data, color='purple')
    plt.title('CO vs Wind Speed', fontsize=16, fontweight='bold')
    plt.xlabel('Wind Speed (m/s)', fontsize=12)
    plt.ylabel('CO (µg/m³)', fontsize=12)

    plt.tight_layout()
    st.pyplot()

    st.markdown("""
        ### Observations:
        - It is observed that higher wind speeds have a negative correlation with polutants. 
        - THis is because wind might help disperse the polutant away. For O3, the correlation is very small.
        """)
elif optional_eda == "Correlation Anlysis of DEw Point vs. Air Quality":
    st.subheader("Correlation Analysis of DEw Point vs. Air Quality")
    st.markdown("""DEw Point is the dew point temperature. It is the temperature at which water will condense. It is measured in degrees Celsius. """)
    # plot dew point vs. air quality pollutants.

    # Plot PM2.5 vs. Dew Point
    plt.subplot(2, 2, 1)
    sns.scatterplot(x='DEWP', y='PM2.5', data=data, color='purple')
    plt.title('PM2.5 vs Dew Point', fontsize=16, fontweight='bold')
    plt.xlabel('Dew Point (°C)', fontsize=12)
    plt.ylabel('PM2.5 (µg/m³)', fontsize=12)

    # Plot NO2 vs. Dew Point
    plt.subplot(2, 2, 2)
    sns.scatterplot(x='DEWP', y='NO2', data=data, color='yellow')
    plt.title('NO2 vs Dew Point', fontsize=16, fontweight='bold')
    plt.xlabel('Dew Point (°C)', fontsize=12)
    plt.ylabel('NO2 (µg/m³)', fontsize=12)

    # Plot O3 vs. Dew Point
    plt.subplot(2, 2, 3)
    sns.scatterplot(x='DEWP', y='O3', data=data, color='red')
    plt.title('O3 vs Dew Point', fontsize=16, fontweight='bold')
    plt.xlabel('Dew Point (°C)', fontsize=12)
    plt.ylabel('O3 (µg/m³)', fontsize=12)

    # Plot CO vs. Dew Point
    plt.subplot(2, 2, 4)
    sns.scatterplot(x='DEWP', y='CO', data=data, color='green')
    plt.title('CO vs Dew Point', fontsize=16, fontweight='bold')
    plt.xlabel('Dew Point (°C)', fontsize=12)
    plt.ylabel('CO (µg/m³)', fontsize=12)

    plt.tight_layout()
    st.pyplot()

    st.markdown("""### Observations:
        - The scatter plot for `Pm2.5` shows a weak correlation between PM2.5 levels and dew point. We expect more dew points in colder times hence higher PM2.5 might coincide with higher humidity though the relationship is not strong.
        - For the case of `NO2`, it has some moderate correlation between NO2 and dew point. High dew points may trap NO2 closer to the ground, increasing pollution.
        - The scatter plot for `Ozone (O3)` is shows a strong positive correlation with dew point, especially during the summer months. Ozone forms in warm, sunny conditions, and higher dew points indicate high humidity, which can increases ozone formation.
        - The relationship between `CO and dew point` may be weak or non-linear. CO is primarily linked to combustion processes while higher humidity can affect air quality, it’s not as directly tied to CO levels as it is for other pollutants like O3.
                        
        """)

else:
    st.write("Please select an option from the dropdown menu.")
