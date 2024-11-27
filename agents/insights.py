import os
import json

from agents.config import model
from data.data import data

fetched_data = data.get_data()

def get_combined_insights(combined_json_str):
    response = model.generate_content([
    "input: I'll provide you three jsons containing insights pertaining one's health. Combine/summarize them and make a list of insights/recommendations and return in json format.\n\n{  \"overall_analysis\": {    \"suggestion\": \"Your sleep duration is consistently low, averaging around 5.5 hours, which is significantly below the recommended 7-9 hours for optimal health. Additionally, your sleep disturbances are high, averaging over 6 per night, indicating that your sleep quality is poor. The forecasted sleep durations for the coming days suggest minimal improvement. To enhance your sleep, focus on improving sleep hygiene by creating a regular sleep schedule, reducing caffeine and screen time before bed, and creating a calm, dark sleep environment. Prioritize longer sleep durations to promote better overall health.\"  }}{  \"overall_analysis\": {    \"suggestion\": \"Take a small but steady step forward with a 5% increase, bringing your daily target to 3,150 steps. This will gradually boost your activity levels and help build a solid foundation for improved fitness over time. Consistency is key!\"  }}{  \"Sentimental Analysis\": {    \"Summary\": \"Your journal entries reflect a mix of emotions, with one expressing anxiety (negative) and one expressing accomplishment (positive). This week, your entries were 50% positive and 50% negative.\",  }}",
    "output: {\n  \"recommendations\": [\n    \"Improve sleep hygiene by establishing a regular sleep schedule, reducing caffeine and screen time before bed, and creating a calm, dark sleep environment.\",\n    \"Prioritize longer sleep durations to achieve 7-9 hours of sleep for optimal health.\",\n    \"Increase your daily step count by 5%, setting a target of 3,150 steps to gradually boost fitness levels.\",\n    \"Track emotions to manage anxiety and focus on activities that promote a positive mood.\"\n  ]\n}",
    "input: ```json\n{\n  \"overall_analysis\": {\n    \"suggestion\": \"Your average hydration levels are currently below the optimal range, averaging around 1.8 liters per day, while the recommended intake is 2.5-3 liters for your activity level. Increasing your water intake will help with hydration and improve your energy and focus. Aim to gradually increase your daily water consumption by 300-400 milliliters per day to reach the recommended level.\"\n  }\n}\n```\n\n```json\n{\n  \"overall_analysis\": {\n    \"suggestion\": \"Your daily screen time is consistently high, averaging around 7 hours per day, which can negatively impact your sleep and focus. Reducing your screen time by 15-20 minutes per week can help improve your sleep quality and mental well-being. Consider implementing regular screen-free intervals, especially before bed.\"\n  }\n}\n```\n\n```json\n{\n  \"Sentimental Analysis\": {\n    \"Summary\": \"Your journal entries this week display a balance of emotions. 70% of your entries are positive, indicating a sense of accomplishment and satisfaction, while 30% are negative, reflecting stress or frustration. Continue focusing on maintaining the positive outlook and addressing sources of stress proactively.\"\n  }\n}\n```",
    "output: {\n  \"recommendations\": [\n    \"Increase your daily water intake by 300-400 milliliters per day to reach the recommended 2.5-3 liters for optimal hydration, which will improve energy and focus.\",\n    \"Gradually reduce your daily screen time by 15-20 minutes per week to improve sleep quality and mental well-being. Implement regular screen-free intervals, especially before bed.\",\n    \"Focus on maintaining a positive outlook, as 70% of your journal entries are positive, indicating accomplishment and satisfaction. Proactively address sources of stress or frustration to maintain mental balance.\",\n    \"Create a consistent sleep schedule, reduce caffeine and screen time before bed, and aim for 7-9 hours of sleep per night to improve overall health and energy.\"\n  ]\n}",
    "input: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Your weekly physical activity is currently low, averaging only 15 minutes of exercise per day. The recommended amount for health benefits is at least 30 minutes of moderate exercise daily. Start by adding short, manageable sessions of 10-15 minutes and gradually increase your workout time. Consistency is key to improving fitness and overall health.\"\n  }\n}\n\n{\n  \"overall_analysis\": {\n    \"suggestion\": \"Your nutrient intake is not well-balanced, with a higher consumption of processed foods and low intake of vegetables and fruits. Aim to increase your daily vegetable intake by incorporating them into each meal. A steady improvement in your diet will enhance your energy levels and overall well-being.\"\n  }\n}\n\n{\n  \"Sentimental Analysis\": {\n    \"Summary\": \"Your journal entries reflect a predominance of positive emotions, with 80% expressing feelings of gratitude and contentment, while 20% indicate mild frustration. Focus on acknowledging and celebrating your achievements to maintain a positive mindset.\"\n  }\n}",
    "output: ```json\n{\n  \"recommendations\": [\n    \"Increase your daily physical activity to at least 30 minutes of moderate exercise, starting with short, manageable sessions and gradually increasing the duration.\",\n    \"Improve your diet by increasing your daily intake of vegetables and fruits, aiming for their inclusion in each meal to enhance energy levels and overall well-being.\",\n    \"Maintain your positive mindset by acknowledging and celebrating achievements, as your journal entries reflect predominantly positive emotions (80% gratitude and contentment).\",\n    \"Address sources of mild frustration (20% of journal entries) to further enhance mental well-being.\"\n  ]\n}\n```",
    "input: {\n  \"overall_analysis\": {\n    \"suggestion\": \"Your stress levels are consistently high, with an average stress score of 7/10. To better manage stress, incorporate relaxation techniques such as deep breathing, meditation, or yoga into your daily routine. Start with 10-minute sessions and gradually increase the duration to help reduce overall stress and improve mental clarity.\"\n  }\n}\n\n{\n  \"overall_analysis\": {\n    \"suggestion\": \"Your sleep consistency is lacking, with irregular bedtimes and wake times. Establishing a more consistent sleep schedule, aiming to go to bed and wake up at the same time every day, will improve the quality and duration of your sleep. Focus on gradual adjustments to align with a healthier routine.\"\n  }\n}\n\n{\n  \"Sentimental Analysis\": {\n    \"Summary\": \"Your journal entries reveal a predominantly positive emotional trend this week, with 85% expressing optimism and satisfaction. The remaining 15% reflects moments of uncertainty. Continue fostering positive reflections and addressing any uncertainties with proactive steps.\"\n  }\n}",
    "output: ```json\n{\n  \"recommendations\": [\n    \"Incorporate relaxation techniques like deep breathing, meditation, or yoga (starting with 10-minute sessions) into your daily routine to manage consistently high stress levels.\",\n    \"Establish a consistent sleep schedule with regular bedtimes and wake times to improve sleep quality and duration. Make gradual adjustments to align with a healthier routine.\",\n    \"Maintain your predominantly positive emotional outlook (85% optimism and satisfaction) by continuing to foster positive reflections in your journal.\",\n    \"Proactively address the remaining 15% of journal entries reflecting uncertainty to further enhance mental well-being.\"\n  ]\n}\n```",
    f"input: {combined_json_str}",
    "output: ",
    ])

    # Remove the triple backticks and JSON block declaration
    cleaned_resp = response.text.strip("```json\n").strip("```")

    # Convert the cleaned string into a Python dictionary
    real_dict = json.loads(cleaned_resp)

    # Return listn of recommendations
    return real_dict["recommendations"]
