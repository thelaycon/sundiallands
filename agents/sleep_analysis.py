import json
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from data.data import data

fetched_data = data.get_data()

def extract_metrics():
    # Extracting the metrics list from the JSON
    metrics = fetched_data.get("metrics", [])

    # List to store the extracted data
    extracted_data = []

    for entry in metrics:
        # Extract the relevant information
        date = entry.get("date")
        sleep_duration = entry.get("sleep_data", {}).get("duration")
        
        # Create a dictionary for each entry
        data_entry = {
            "date": date,
            "sleep_duration": sleep_duration,
        }

        # Add the data entry to the list
        extracted_data.append(data_entry)

    return extracted_data

def prepare_data_for_arima(extracted_data, column):
    # Convert the extracted data into a pandas DataFrame
    df = pd.DataFrame(extracted_data)

    # Convert 'date' column to datetime format and ensure it's a datetime index
    df['date'] = pd.to_datetime(df['date'])
    
    # Set 'date' as the index and ensure that the frequency is daily
    df.set_index('date', inplace=True)
    df = df.asfreq('D')  # Set the frequency to daily (adjust if needed)

    # Select the specified column for forecasting (e.g., 'sleep_duration')
    time_series_data = df[column]

    return time_series_data


def forecast_with_arima(time_series_data, steps_ahead=5):
    # Fit the ARIMA model
    model = ARIMA(time_series_data, order=(1, 1, 0))  
    model_fit = model.fit()

    # Make predictions for the next 'steps_ahead' days
    forecast = model_fit.forecast(steps=steps_ahead)

    # Create a forecasted time index based on the last date in the series
    last_date = time_series_data.index[-1]
    forecast_dates = pd.date_range(start=last_date, periods=steps_ahead + 1, freq='D')[1:]

    # Create a DataFrame with the forecasted dates and values
    forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'forecast': forecast
    })

    return forecast_df

def forecast(days=7):
    # Extract the metrics
    extracted_metrics = extract_metrics()

    # Prepare the data for ARIMA (forecasting 'sleep_duration')
    time_series_data = prepare_data_for_arima(extracted_metrics, column='sleep_duration')

    # Apply ARIMA to forecast future 'sleep_duration' values
    forecast_df = forecast_with_arima(time_series_data, steps_ahead=days)

    # Convert the DataFrame to a JSON string
    forecast_json_str = forecast_df.to_json(orient='records', date_format='iso')
    
    return forecast_json_str

# # Example usage:
# forecast_json_str = forecast(days=7)
# print(forecast_json_str)
