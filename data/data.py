import json
from data.normalize import HealthData

class Data:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} does not exist.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file {self.file_path}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_data(self):
        return self.data

# Load the JSON data from a file
health_data = HealthData.load_from_file("data/health_data.json")

# Normalize all metrics
normalized_data = health_data.normalize_all()

# Save the normalized data back to a file
health_data.save_to_file("data/normalized_health_data.json")

data = Data("data/normalized_health_data.json")
