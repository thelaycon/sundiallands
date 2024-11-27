import json
import joblib

import pandas as pd
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
        calories_burned = entry.get("calories_burned", None)
        active_minutes = entry.get("active_minutes", None)
        steps_taken = entry.get("steps", None)
        
        # Create a dictionary for each entry
        data_entry = {
            "Date": date,
            "Calories Burned": calories_burned,
            "Active Minutes": active_minutes,
            "Steps Taken": steps_taken
        }

        # Add the data entry to the list
        extracted_data.append(data_entry)

    return extracted_data

def get_last_days_fitness_data(days=7):
    # Extract the metrics
    extracted_metrics = extract_metrics()

    # Convert the extracted data into a pandas DataFrame
    df = pd.DataFrame(extracted_metrics)

    # Convert 'date' column to datetime format and ensure it's a datetime index
    df['Date'] = pd.to_datetime(df['Date'])

    # Set 'date' as the index
    df.set_index('Date', inplace=True)

    # Get the last 'days' of fitness data
    last_days_data = df.tail(days)  # Get the last 'days' records
    
    return last_days_data


def recommend_steps(user_data, model_path='models/fitness/fitness_kmeans_model.pkl', scaler_path='models/fitness/fitness_scaler.pkl'):
    # Recommend new target steps based on a user's activity data.
    
    # Load the saved model and scaler
    loaded_kmeans = joblib.load(model_path)
    loaded_scaler = joblib.load(scaler_path)

    # Convert user data to a DataFrame
    user_df = pd.DataFrame([user_data])

    # Standardize user data
    user_scaled = loaded_scaler.transform(user_df)

    # Predict cluster for the user
    user_cluster = loaded_kmeans.predict(user_scaled)[0]

    # Recommendations based on cluster
    recommendations = {
        0: 0.05,  # Sedentary
        1: 0.10,  # Moderately Active
        2: 0.15   # Highly Active
    }
    recommended_increase = recommendations[user_cluster]

    # Calculate new target steps
    current_steps = user_data['Steps']
    new_steps_target = int(current_steps * (1 + recommended_increase))
    
    result = {
        "Recommended_Increase": recommended_increase,
        "New_Target_Steps": new_steps_target
    }

    combined_json_str = json.dumps(result, indent=4, default=str)

    return combined_json_str


def analyze_fitness(recommended_steps):
    response = model.generate_content([
        "input: You're a fitness analyser. I'll provide information such as {\n    \"Recommended_Increase\": 0.05,\n    \"New_Target_Steps\": 6000\n}  \nand you will give Output: Analyze activity patterns and provide workout suggestions.\nExample: \"Increase your weekly activity by 10% to improve cardiovascular health.\"\n\noutput should be as json in this form\n\n{\n  \"overall_analysis\": {\n    \"suggestion\": \"\"\n  }\n}",
        "output: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Increase your daily steps by 5% to gradually improve cardiovascular fitness. Aim for 6,300 steps daily to enhance endurance and maintain a healthy activity level.\"\n  }\n}",
        "input: {\n    \"Recommended_Increase\": 0.1,\n    \"New_Target_Steps\": 6600\n}",
        "output: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Challenge yourself to a 10% boost in daily steps—take it to 6,600 steps! This increase will help elevate your energy levels, improve your heart health, and keep you feeling strong and active throughout the day. Small steps today, big gains tomorrow!\"\n  }\n}",
        "input: {\n    \"Recommended_Increase\": 0.1,\n    \"New_Target_Steps\": 4400\n}",
        "output: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Step it up with a 10% increase! Aim for 4,400 steps daily—an achievable target that will steadily improve your stamina and kick-start a healthier routine. Small steps now will lay the foundation for lasting fitness progress!\"\n  }\n}",
        "input: {\n    \"Recommended_Increase\": 0.05,\n    \"New_Target_Steps\": 3150\n}",
        "output: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Take a small but steady step forward with a 5% increase, bringing your daily target to 3,150 steps. This will gradually boost your activity levels and help build a solid foundation for improved fitness over time. Consistency is key!\"\n  }\n}",
        "input: {\n    \"Recommended_Increase\": 0.1,\n    \"New_Target_Steps\": 11\n}",
        "output: ```json\n{\n  \"overall_analysis\": {\n    \"suggestion\": \"Increase your daily steps by 10%, aiming for 11 steps. While this is a small number, even incremental increases in activity can contribute to overall well-being. Consider incorporating short walks or movement breaks throughout your day to gradually increase your step count.\"\n  }\n}\n```",
        f"input: be creative {recommended_steps}",
        "output: ",
        ])
    
    # Remove the triple backticks and JSON block declaration
    cleaned_resp = response.text.strip("```json\n").strip("```")

    # Convert the cleaned string into a Python dictionary
    real_dict = json.loads(cleaned_resp)

    suggestion = real_dict['overall_analysis']['suggestion']

    return suggestion
    
# Fetch the last 7 days of fitness data
last_7_days_data = get_last_days_fitness_data(days=7)

# Summarize the last 7 days' data into a single dictionary for analysis
average_steps = last_7_days_data["Steps Taken"].mean()
average_calories = last_7_days_data["Calories Burned"].mean()
average_active_minutes = last_7_days_data["Active Minutes"].mean()

# Create a user data dictionary for recommendations
user_data = {
    "Steps": int(average_steps),
    "Calories_Burned": int(average_calories),
    "Active_Minutes": int(average_active_minutes),
}

# Generate recommendations based on user data
recommendation_result = recommend_steps(user_data)

# Analyze and generate fitness suggestions
fitness_suggestion = analyze_fitness(recommendation_result)

# Output the last 7 days' data, averages, and suggestions
print("Last 7 Days' Fitness Data:")
print(last_7_days_data)
print("\nAverages:")
print(f"Steps Taken: {average_steps:.2f}")
print(f"Calories Burned: {average_calories:.2f}")
print(f"Active Minutes: {average_active_minutes:.2f}")
print("\nRecommendation Result:")
print(recommendation_result)
print("\nFitness Suggestion:")
print(fitness_suggestion)
