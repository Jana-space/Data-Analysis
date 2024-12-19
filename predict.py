import streamlit as st
import pickle
from app_utils import predict_air_quality


st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .form-container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .form-container h2 {
            font-size: 2rem;
            color: #1e3d58;
        }
        .form-container .form-label {
            font-weight: bold;
        }
        .form-container .btn-primary {
            background-color: #0d6efd;
            border-color: #0d6efd;
        }
        .form-container .btn-primary:hover {
            background-color: #0b5ed7;
            border-color: #0a58ca;
        }
        .message {
            font-weight: bold;
            font-size: 1.5rem;
            color: #0d6efd;
        }
        .error-message {
            font-weight: bold;
            font-size: 1.5rem;
            color: #dc3545;
        }
    body {
    background-color: #ffffff; 
    color: #212529; 
    font-weight: bold;
    
}
    </style>
""", unsafe_allow_html=True)

# load the trained model and other items
model = pickle.load(open('best_gradient_model.pkl', 'rb'))
encoder_wd = pickle.load(open('models/encoder_wd.pkl', 'rb'))
encoder_station = pickle.load(open('models/encoder_station.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))


st.title("Model Prediction Page")
st.write("""
This application uses weather and air quality parameters to predict PM2.5 levels.
""")

col1, colx, col2 = st.columns([2, 1, 2])
with col1:
    year = st.selectbox("Select Year", options=[2013, 2014, 2015, 2016, 2017])
    month = st.selectbox("Select Month", options=[
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    day = st.number_input("Enter Day", min_value=1, max_value=31)
    hour = st.number_input("Enter Hour", min_value=0, max_value=23)

    # Wind direction
    wd = st.selectbox("Select Wind Direction", options=[
        "NE", "ENE", "NW", "N", "E", "SW", "NNE", "NNW", "WNW", "ESE", "SSW", "SE", "WSW", "S", "SSE", "W"])

    # Station
    station = st.selectbox("Select Station", options=["Dongsi", "Changping", "Guanyuan", "Wanshouxigong",
                                                      "Huairou", "Aotizhongxin", "Wanliu", "Tiantan", "Dingling", "Shunyi", "Nongzhanguan", "Gucheng"])
    wspm = st.number_input("Enter WSPM", step=0.1)
    temp = st.number_input("Enter Temperature (°C)", step=0.1)
with col2:
    pres = st.number_input("Enter Pressure (hPa)", step=0.1)
    dewp = st.number_input("Enter Dew Point (°C)", step=0.1)
    rain = st.number_input("Enter Rain (mm)", step=0.1)
    so2 = st.number_input("Enter SO2", step=0.1)
    no2 = st.number_input("Enter NO2", step=0.1)
    co = st.number_input("Enter CO", step=0.1)
    o3 = st.number_input("Enter O3", step=0.1)
    pm10 = st.number_input("Enter PM10", step=0.1)


submit_button = st.button(
    "Predict PM2.5", type="primary", use_container_width=True)

if submit_button:
    user_input = {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'wd': wd,
        'station': station,
        'WSPM': wspm,
        'TEMP': temp,
        'PRES': pres,
        'DEWP': dewp,
        'RAIN': rain,
        "SO2": so2,
        "NO2": no2,
        "CO": co,
        "O3": o3,
        "PM10": pm10,
    }

    prediction = predict_air_quality(
        user_input, model=model, scaler=scaler, encoder_wd=encoder_wd, encoder_station=encoder_station)

    if not prediction[0]:
        st.markdown(
            f'<p class="error-message error text-danger">Error:  {prediction[1]}</p>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<p class="message text-success">{prediction[1]} µg/m³</p>', unsafe_allow_html=True)


st.markdown("---")
st.markdown('[Back to Home](#)')
