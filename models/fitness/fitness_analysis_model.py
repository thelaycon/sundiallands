import joblib
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from data.data import data

fetched_data = data.get_data()

def extract_metrics(raw_data):
    # Extracts steps, calories burned, and active minutes from the input data.

    # Initialize the result dictionary
    data = {
        'Steps': [],
        'Calories_Burned': [],
        'Active_Minutes': []
    }
    
    # Extract metrics
    for metric in raw_data.get("metrics", []):
        data['Steps'].append(metric.get("steps", 0))  # Default to 0 if missing
        data['Calories_Burned'].append(metric.get("calories_burned", 0))
        data['Active_Minutes'].append(metric.get("active_minutes", 0))
    
    return data

# Transform data
data = extract_metrics(fetched_data) # Ideally this should be from collected data and not that of the user

# Convert to DataFrame
df = pd.DataFrame(data)

# Standardize the features for clustering
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Apply k-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(scaled_data)

# Save the k-Means model
joblib.dump(kmeans, 'fitness_kmeans_model.pkl')

# Save the scaler
joblib.dump(scaler, 'fitness_scaler.pkl')

print("Model and scaler saved successfully!")


# # Assign percentage increases based on cluster
# # (Values can be adjusted based on domain expertise)
# recommendations = {
#     0: 0.05,  # Sedentary: 5% increase
#     1: 0.10,  # Moderately Active: 10% increase
#     2: 0.15   # Highly Active: 15% increase
# }

# df['Increase_Percentage'] = df['Cluster'].map(recommendations)

# # Example: User data
# user_data = {'Steps': 6000, 'Calories_Burned': 1900, 'Active_Minutes': 50}
# user_df = pd.DataFrame([user_data])

# # Standardize user data
# user_scaled = scaler.transform(user_df)

# # Predict cluster for the user
# user_cluster = kmeans.predict(user_scaled)[0]
# user_recommendation = recommendations[user_cluster]

# # Calculate new target steps
# current_steps = user_data['Steps']
# new_steps_target = int(current_steps * (1 + user_recommendation))

# print(f"User's Cluster: {user_cluster}")
# print(f"Recommended Increase: {user_recommendation * 100}%")
# print(f"New Target Steps: {new_steps_target}")
