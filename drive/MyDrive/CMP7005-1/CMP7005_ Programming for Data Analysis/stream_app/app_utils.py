import pandas as pd
import pickle

import warnings
warnings.filterwarnings("ignore")


def predict_air_quality(user_input, model, scaler, encoder_wd, encoder_station):
    """
    Function to make predictions on air quality data based on user input.

    Parameters:
    user_input (dict): A dictionary with keys as the feature names and values as the feature data.
    model (sklearn model): The trained model (e.g., a regressor or classifier).
    scaler (sklearn transformer): The fitted scaler used for scaling the input data.
    encoder_wd (sklearn encoder): The fitted encoder for the 'wd' (wind direction) feature.
    encoder_station (sklearn encoder): The fitted encoder for the 'station' feature.

    Returns:
    float: The predicted value (e.g., PM2.5, PM10, etc.) based on the model.
    """

    if user_input["wd"] not in encoder_wd.classes_:
        return False, f"YOur WD Input {user_input['wd']} Is incorrect, available wind directions are {list(encoder_wd.classes_)}"

    if user_input["station"] not in encoder_station.classes_:
        return False, f"YOur Station Input {user_input['wd']} Is incorrect, available wind directions are {list(encoder_station.classes_)}"

    # convert user input dictionary to DataFrame
    user_df = pd.DataFrame([user_input])

    # encode categorical features (wind direction and station)
    user_df['wd'] = encoder_wd.transform(user_df['wd'].values.reshape(-1, 1))
    user_df['station'] = encoder_station.transform(
        user_df['station'].values.reshape(-1, 1))

    # Scaling the features
    scaled_data = scaler.transform(user_df[['year', 'month', 'day', 'hour', 'PM10', 'SO2', 'NO2', 'CO',
                                            'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM', 'station']])

    # Make prediction
    prediction = model.predict(scaled_data)

    return True, f"Predicted PM2.5:  {prediction[0]}   µg/m³"


if __name__ == "__main__":
    model = pickle.load(open('models/best_gradient_model.pkl', 'rb'))
    encoder_wd = pickle.load(open('models/encoder_wd.pkl', 'rb'))
    encoder_station = pickle.load(open('models/encoder_station.pkl', 'rb'))
    scaler = pickle.load(open('models/scaler.pkl', 'rb'))
    user_input = {
        'year': 2013,
        'month': 3,
        'day': 1,
        'hour': 0,
        'PM10': 9.0,
        'SO2': 3.0,
        'NO2': 17.0,
        'CO': 300.0,
        'O3': 89.0,
        'TEMP': -0.5,
        'PRES': 1024.5,
        'DEWP': -21.4,
        'RAIN': 0.0,
        'wd': 'SSW',
        'WSPM': 5.7,
        'station': 'Dongsi',
    }

    prediction = predict_air_quality(
        user_input, model, scaler, encoder_wd, encoder_station)
    if not prediction[0]:
        print(prediction[1])
    else:
        print(f"Predicted PM2.5: {prediction[1]}")
