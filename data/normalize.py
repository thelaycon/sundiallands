import json

class HealthData:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def load_from_file(file_path):
        """
        Load data from a JSON file.
        """
        with open(file_path, "r") as f:
            data = json.load(f)
        return HealthData(data)

    def normalize_steps(self, max_steps=10000):
        """
        Normalize steps to a range of 0 to 1 based on a maximum step threshold.
        """
        for metric in self.data["metrics"]:
            metric["normalized_steps"] = metric["steps"] / max_steps
        return self.data

    def normalize_heart_rate(self, min_hr=60, max_hr=80):
        """
        Normalize heart rate to a range of 0 to 1 based on healthy heart rate thresholds.
        """
        for metric in self.data["metrics"]:
            metric["normalized_heart_rate"] = (metric["heart_rate"] - min_hr) / (max_hr - min_hr)
        return self.data

    def normalize_sleep_hours(self, ideal_sleep=8):
        """
        Normalize sleep duration to a range of 0 to 1 based on an ideal sleep threshold.
        """
        for metric in self.data["metrics"]:
            if "sleep_data" in metric and "duration" in metric["sleep_data"]:
                metric["normalized_sleep_hours"] = metric["sleep_data"]["duration"] / ideal_sleep
        return self.data

    def normalize_hrv(self, max_hrv=50):
        """
        Normalize HRV (Heart Rate Variability) to a range of 0 to 1 based on a maximum HRV threshold.
        """
        for metric in self.data["metrics"]:
            metric["normalized_hrv"] = metric["hrv"] / max_hrv
        return self.data

    def normalize_all(self):
        """
        Normalize all metrics in the dataset.
        """
        self.normalize_steps()
        self.normalize_heart_rate()
        self.normalize_sleep_hours()
        self.normalize_hrv()
        return self.data

    def save_to_file(self, output_path):
        """
        Save normalized data to a JSON file.
        """
        with open(output_path, "w") as f:
            json.dump(self.data, f, indent=4)


# Load the JSON data from a file
health_data = HealthData.load_from_file("data/health_data.json")

# Normalize all metrics
normalized_data = health_data.normalize_all()

# Save the normalized data back to a file
health_data.save_to_file("data/normalized_health_data.json")
