import json
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

from agents.config import model
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
        sleep_disturbances = entry.get("sleep_data", {}).get("disturbances")
        
        # Create a dictionary for each entry
        data_entry = {
            "date": date,
            "sleep_duration": sleep_duration,
            "sleep_disturbances": sleep_disturbances
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

def get_last_days_sleep_data(days=7):
    # Extract the metrics
    extracted_metrics = extract_metrics()

    # Convert the extracted data into a pandas DataFrame
    df = pd.DataFrame(extracted_metrics)

    # Convert 'date' column to datetime format and ensure it's a datetime index
    df['date'] = pd.to_datetime(df['date'])

    # Set 'date' as the index
    df.set_index('date', inplace=True)

    # Get the last 'days' of sleep data
    last_days_data = df.tail(days)  # Get the last 'days' records
    
    # Return the last days data as a list of dictionaries
    return last_days_data.to_dict(orient='records')

def forecast_and_combine(days=7):
    # Step 1: Extract the metrics and prepare the data for ARIMA (forecasting 'sleep_duration')
    extracted_metrics = extract_metrics()
    time_series_data = prepare_data_for_arima(extracted_metrics, column='sleep_duration')

    # Step 2: Apply ARIMA to forecast future 'sleep_duration' values
    forecast_df = forecast_with_arima(time_series_data, steps_ahead=days)

    # Step 3: Get the last 'days' of sleep data
    last_days_data = get_last_days_sleep_data(days)

    # Step 4: Combine the last sleep data with the forecasted data
    combined_data = last_days_data + forecast_df.to_dict(orient='records')

    # Step 5: Convert the combined data to JSON string
    combined_json_str = json.dumps(combined_data, indent=4, default=str)

    return combined_json_str


def analyze_sleep():
    # Get historical and forecast values
    forecast_json_str = forecast_and_combine(days=7)

    response = model.generate_content([
        "input: You're a sleep analyser. I'll provide a json input containing Sleep data (duration, disturbances) and forecasted values by ARIMA. \nOutput: Detect poor sleep patterns and suggest improvements.\nExample: \"Your average sleep time has dropped below 6 hours. Consider a consistent bedtime routine.\"\n\nThe output should be in json always.\n\nuse the data below as an example:\n\n[\n    {\n        \"sleep_duration\": 7.5,\n        \"sleep_disturbances\": 1\n    },\n    {\n        \"sleep_duration\": 6.1,\n        \"sleep_disturbances\": 3\n    },\n    {\n        \"sleep_duration\": 6.8,\n        \"sleep_disturbances\": 2\n    },\n    {\n        \"sleep_duration\": 7.0,\n        \"sleep_disturbances\": 1\n    },\n    {\n        \"sleep_duration\": 5.5,\n        \"sleep_disturbances\": 5\n    },\n    {\n        \"sleep_duration\": 7.8,\n        \"sleep_disturbances\": 1\n    },\n    {\n        \"sleep_duration\": 6.0,\n        \"sleep_disturbances\": 3\n    },\n    {\n        \"date\": \"2024-11-23 00:00:00\",\n        \"forecast\": 14.852777353397855\n    },\n    {\n        \"date\": \"2024-11-24 00:00:00\",\n        \"forecast\": 12.02491605664364\n    },\n    {\n        \"date\": \"2024-11-25 00:00:00\",\n        \"forecast\": 13.862087789637975\n    },\n    {\n        \"date\": \"2024-11-26 00:00:00\",\n        \"forecast\": 12.668535623417014\n    },\n    {\n        \"date\": \"2024-11-27 00:00:00\",\n        \"forecast\": 13.443948584495454\n    },\n    {\n        \"date\": \"2024-11-28 00:00:00\",\n        \"forecast\": 12.940187393971065\n    },\n    {\n        \"date\": \"2024-11-29 00:00:00\",\n        \"forecast\": 13.267465050931559\n    }\n]",
        "output: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Your average sleep duration is below the recommended range, and you have frequent disturbances. It's essential to aim for 7-9 hours of sleep per night and reduce disturbances by improving your sleep environment. The forecasted values indicate unusually long sleep durations in the coming days, which could reflect irregular sleep patterns. To optimize your sleep, focus on establishing a consistent sleep schedule, limit screen exposure before bed, and create a calming bedtime routine to promote uninterrupted sleep.\"\n  }\n}",
        "input: [\n    {\n        \"sleep_duration\": 8.0,\n        \"sleep_disturbances\": 1\n    },\n    {\n        \"sleep_duration\": 7.0,\n        \"sleep_disturbances\": 3\n    },\n    {\n        \"sleep_duration\": 7.2,\n        \"sleep_disturbances\": 2\n    },\n    {\n        \"sleep_duration\": 7.3,\n        \"sleep_disturbances\": 1\n    },\n    {\n        \"sleep_duration\": 6.0,\n        \"sleep_disturbances\": 4\n    },\n    {\n        \"sleep_duration\": 8.2,\n        \"sleep_disturbances\": 1\n    },\n    {\n        \"sleep_duration\": 6.3,\n        \"sleep_disturbances\": 2\n    },\n    {\n        \"date\": \"2024-11-23 00:00:00\",\n        \"forecast\": 7.607278766208423\n    },\n    {\n        \"date\": \"2024-11-24 00:00:00\",\n        \"forecast\": 7.915738701149979\n    },\n    {\n        \"date\": \"2024-11-25 00:00:00\",\n        \"forecast\": 7.673461168698944\n    },\n    {\n        \"date\": \"2024-11-26 00:00:00\",\n        \"forecast\": 7.863756231627243\n    },\n    {\n        \"date\": \"2024-11-27 00:00:00\",\n        \"forecast\": 7.714290407831949\n    },\n    {\n        \"date\": \"2024-11-28 00:00:00\",\n        \"forecast\": 7.8316872132930735\n    },\n    {\n        \"date\": \"2024-11-29 00:00:00\",\n        \"forecast\": 7.739478776725308\n    }\n]",
        "output: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Your sleep duration is generally within the recommended range, but there are occasional disturbances that can affect sleep quality. The forecasted values for the upcoming days suggest a consistent sleep pattern around 7.7 hours, which is ideal. To further improve your sleep, maintain your current sleep duration while working on reducing disturbances. Consider implementing relaxation techniques before bed, such as meditation or deep breathing, to minimize interruptions and ensure more restful sleep.\"\n  }\n}",
        "input: [\n    {\n        \"sleep_duration\": 4.0,\n        \"sleep_disturbances\": 8\n    },\n    {\n        \"sleep_duration\": 5.5,\n        \"sleep_disturbances\": 7\n    },\n    {\n        \"sleep_duration\": 8.0,\n        \"sleep_disturbances\": 3\n    },\n    {\n        \"sleep_duration\": 5.8,\n        \"sleep_disturbances\": 6\n    },\n    {\n        \"sleep_duration\": 4.2,\n        \"sleep_disturbances\": 7\n    },\n    {\n        \"sleep_duration\": 6.5,\n        \"sleep_disturbances\": 5\n    },\n    {\n        \"sleep_duration\": 4.7,\n        \"sleep_disturbances\": 7\n    },\n    {\n        \"date\": \"2024-11-23 00:00:00\",\n        \"forecast\": 5.5053143899860615\n    },\n    {\n        \"date\": \"2024-11-24 00:00:00\",\n        \"forecast\": 5.750028242740925\n    },\n    {\n        \"date\": \"2024-11-25 00:00:00\",\n        \"forecast\": 5.6289718212120246\n    },\n    {\n        \"date\": \"2024-11-26 00:00:00\",\n        \"forecast\": 5.688856690942153\n    },\n    {\n        \"date\": \"2024-11-27 00:00:00\",\n        \"forecast\": 5.659232507629099\n    },\n    {\n        \"date\": \"2024-11-28 00:00:00\",\n        \"forecast\": 5.673887164822482\n    },\n    {\n        \"date\": \"2024-11-29 00:00:00\",\n        \"forecast\": 5.666637716789228\n    }\n]",
        "output: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Your sleep duration is consistently low, averaging around 5.5 hours, which is significantly below the recommended 7-9 hours for optimal health. Additionally, your sleep disturbances are high, averaging over 6 per night, indicating that your sleep quality is poor. The forecasted sleep durations for the coming days suggest minimal improvement. To enhance your sleep, focus on improving sleep hygiene by creating a regular sleep schedule, reducing caffeine and screen time before bed, and creating a calm, dark sleep environment. Prioritize longer sleep durations to promote better overall health.\"\n  }\n}",
        "input: [\n    {\n        \"sleep_duration\": 4.2,\n        \"sleep_disturbances\": 6\n    },\n    {\n        \"sleep_duration\": 4.5,\n        \"sleep_disturbances\": 6\n    },\n    {\n        \"sleep_duration\": 4.8,\n        \"sleep_disturbances\": 6\n    },\n    {\n        \"sleep_duration\": 5.2,\n        \"sleep_disturbances\": 5\n    },\n    {\n        \"sleep_duration\": 4.0,\n        \"sleep_disturbances\": 7\n    },\n    {\n        \"sleep_duration\": 4.3,\n        \"sleep_disturbances\": 6\n    },\n    {\n        \"sleep_duration\": 4.1,\n        \"sleep_disturbances\": 7\n    },\n    {\n        \"date\": \"2024-11-23 00:00:00\",\n        \"forecast\": 3.727552890475691\n    },\n    {\n        \"date\": \"2024-11-24 00:00:00\",\n        \"forecast\": 3.8760077454519926\n    },\n    {\n        \"date\": \"2024-11-25 00:00:00\",\n        \"forecast\": 3.7951155531857053\n    },\n    {\n        \"date\": \"2024-11-26 00:00:00\",\n        \"forecast\": 3.8391932411177745\n    },\n    {\n        \"date\": \"2024-11-27 00:00:00\",\n        \"forecast\": 3.815175563774561\n    },\n    {\n        \"date\": \"2024-11-28 00:00:00\",\n        \"forecast\": 3.8282626573138527\n    },\n    {\n        \"date\": \"2024-11-29 00:00:00\",\n        \"forecast\": 3.821131575700144\n    }\n]",
        "output: ```json\n{\n  \"overall_analysis\": {\n    \"suggestion\": \"Your sleep duration is significantly below the recommended 7-9 hours, and you experience a high number of disturbances.  The forecasted sleep durations are also very low. This indicates a serious sleep problem.  You should consult a doctor or sleep specialist to address the underlying causes of your poor sleep.  In the meantime, try to establish a regular sleep schedule, create a relaxing bedtime routine, and ensure your sleep environment is dark, quiet, and cool.  Avoid caffeine and alcohol before bed. Addressing the high number of disturbances is crucial; consider keeping a sleep diary to identify potential triggers.\"\n  }\n}\n```",
        f"input: {forecast_json_str}",
        "output: ",
        ])
    
    # Remove the triple backticks and JSON block declaration
    cleaned_resp = response.text.strip("```json\n").strip("```")

    # Convert the cleaned string into a Python dictionary
    real_dict = json.loads(cleaned_resp)

    # Print the resulting dictionary
    return real_dict

print(analyze_sleep())