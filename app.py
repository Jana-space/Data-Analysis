import streamlit as st

st.set_page_config(page_title="Air Quality App", layout="wide")

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

st.html("""
<body class="">
    <div class="container py-5">
        <div class="row justify-content-center text-center">
            <div class="col-lg-10">
                <h1 class="display-4 text-primary mb-4">Welcome to Air Quality Analysis and Prediction</h1>
                <p class="lead text-secondary mb-5">This application uses Plotting tools and machine learning to predict
                    PM2.5 levels based on weather parameters and various air quality indicators.
                    Explore the dataset, perform exploratory data analysis (EDA), and use the models for making
                    predictions about air quality.</p>

                <div class="my-4">
                    <a href="/data_overview" class="btn btn-lg btn-info mx-2">Data Overview</a>
                    <a href="/eda" class="btn btn-lg btn-info mx-2">Exploratory Data Analysis (EDA)</a>
                    <a href="/predict" class="btn btn-lg btn-success mx-2">Model Prediction</a>
                    <a href="/project" class="btn btn-lg btn-primary mx-2">Project Implmentation</a>
                </div>

                <div class="row mt-5">
                    <div class="col-md-6">
                        <h4 class="text-primary">About the Dataset</h4>
                        <p class="text-muted">The dataset contains air quality measurements from Beijing over a period
                            from March 1st, 2013, to February 28th, 2017.
                            The data includes various air quality indicators such as PM2.5, PM10, SO2, NO2, CO, O3, and
                            weather-related features like temperature, pressure, wind direction, and more.</p>
                    </div>
                    <div class="col-md-6 row">
                        <h4 class="text-primary">Air Quality Stations</h4>
                        <p class="text-muted">The data was collected from various air quality monitoring stations across
                            Beijing.
                            These stations are located in different areas of the city and provide valuable insights into
                            how air pollution levels vary across regions.</p>
                    </div>
                    
                    <div class="col-md-12">
                        <ul class="list-group mr-auto mb-5 " style="list-style: none; padding: 0; font-size: 17px; font-weight: 500">
                            <li class="list-item">Dongsi</li>
                            <li class="list-item">Changping</li>
                            <li class="list-item">Guanyuan</li>
                            <li class="list-item">Wanshouxigong</li>
                            <li class="list-item">Huairou</li>
                            <li class="list-item">Aotizhongxin</li>
                            <li class="list-item">Wanliu</li>
                            <li class="list-item">Tiantan</li>
                            <li class="list-item">Dingling</li>
                            <li class="list-item">Shunyi</li>
                            <li class="list-item">Nongzhanguan</li>
                            <li class="list-item">Gucheng</li>
                        </ul>
                    </div>
                </div>
                </div>

                <div class="mt-5">
                    <h4 class="text-primary">Goal of the Application</h4>
                    <p class="text-muted">The purpose of this application is to predict the concentration of PM2.5
                        (particulate matter smaller than 2.5 micrometers) based on weather and air quality data.
                        The PM2.5 is an important indicator of air pollution, and predicting its levels can help
                        mitigate health risks and inform public policies.</p>
                </div>
                <div class="mt-5">
                    <h4 class="text-primary">Future Work</h4>
                    <p class="text-muted">The application can be expanded with more advanced machine learning models,
                        real-time data collection, and predictions for different pollutants.
                        Integration with external APIs can also be explored to provide live air quality updates.</p>
                </div>

            </div>
        </div>
    </div>
</body>
""")
