import json
import joblib

import pandas as pd
from agents.config import model

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

    # Print the resulting dictionary
    return real_dict
    
# Example usage:
new_user_data = {'Steps': 10, 'Calories_Burned': 0, 'Active_Minutes': 55}
result = recommend_steps(new_user_data)

print(analyze_fitness(result))