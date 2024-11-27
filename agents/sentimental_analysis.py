import os
import json

from agents.config import model
from data.data import data

fetched_data = data.get_data()

def extract_journal_entries():
    # Extract journal entries from a JSON file and format them into the specified structure.
    
    # Extract user_id and journal entries
    user_id = fetched_data.get("user_id", "unknown")
    journal_entries = fetched_data.get("journal_entries", [])
    
    # Create the desired structure
    formatted_data = {
        "user_id": user_id,
        "journal_entries": journal_entries
    }
    
    # Convert to a JSON string
    formatted_string = json.dumps(formatted_data, indent=4)
    return formatted_string



def sentimentalize():
    # Get journal entries
    journal_entries = extract_journal_entries()
    
    response = model.generate_content([
        "input: You're a sentimental analysis. I'll give you a json of journal entries and you'll perform a sentimental analysis. \n\n{\n\"user_id\": \"12345\",\n\"journal_entries\": [\n  {\n\"date\": \"2024-11-22\",\n\"entry\": \"I feel really anxious about the upcoming presentation. It's overwhelming.\"\n   },\n  {\n\"date\": \"2024-11-21\",\n\"entry\": \"Had a great day today! Felt accomplished after finishing all my tasks.\"\n    }\n ]\n}\n\nOutput: Perform sentiment analysis to extract emotional tone (positive, negative, neutral) and provide emotional feedback.\nExample: \"Your recent journal entries reflect sadness. Would you like some tips for managing negative emotions?\" or Summarize user emotions over a period (e.g., \"Your journal entries this week were 70% positive, 30% negative.\").\n\ngive output in json containing 1 value 1. Sentimental Analysis.",
        "output: {\n  \"Sentimental Analysis\": {\n    \"Summary\": \"Your journal entries reflect a mix of emotions, with one expressing anxiety (negative) and one expressing accomplishment (positive). This week, your entries were 50% positive and 50% negative.\",\n    \"Feedback\": \"It seems like you experienced some stress about your presentation but also had a sense of achievement on another day. Would you like support with managing stress or strategies to enhance positive experiences?\"\n  }\n}",
        "input: {\n\"user_id\": \"12345\",\n\"journal_entries\": [\n  {\n\"date\": \"2024-11-22\",\n\"entry\": \"I am afraid of working out.\"\n   },\n  {\n\"date\": \"2024-11-21\",\n\"entry\": \"The gym just broke up.\"\n    }\n ]\n}",
        "output: ```json\n{\n  \"Sentimental Analysis\": {\n    \"Summary\": \"Your journal entries this week reflect primarily negative emotions.  Both entries express fear and disappointment related to working out and the gym.\",\n    \"Feedback\": \"It seems you're experiencing some negativity around working out.  Would you like some suggestions for overcoming your fear or finding alternative ways to stay active?\"\n  }\n}\n```",
        "input: You can add statistics too. Like 50% negativity, etc\n\n{\n\"user_id\": \"12345\",\n\"journal_entries\": [\n  {\n\"date\": \"2024-11-22\",\n\"entry\": \"I am eager of working out. \"\n   },\n  {\n\"date\": \"2024-11-21\",\n\"entry\": \"The gym just broke up, but I fixed it. LFG!!!!\"\n    }\n ]\n}",
        "output: ```json\n{\n  \"Sentimental Analysis\": {\n    \"Summary\": \"Your journal entries this week reflect primarily positive emotions. One entry expresses eagerness about working out, and the other expresses accomplishment and excitement after fixing a broken gym.  This week, your entries were 100% positive.\",\n    \"Feedback\": \"It's great to see such positive emotions in your journal entries!  Keep up the positive attitude and proactive problem-solving.\"\n  }\n}\n```",
        "input: {\n\"user_id\": \"12345\",\n\"journal_entries\": [\n  {\n\"date\": \"2024-11-22\",\n\"entry\": \"I am eager of working out. \"\n   },\n  {\n\"date\": \"2024-11-21\",\n\"entry\": \"I've been eating too much McDonalds\"\n    }\n ]\n}",
        "output: ```json\n{\n  \"Sentimental Analysis\": {\n    \"Summary\": \"Your journal entries show a mix of positive and negative emotions this week. One entry expresses eagerness about working out (positive), while the other expresses guilt or dissatisfaction about eating too much fast food (negative). This week, your entries were 50% positive and 50% negative.\",\n    \"Feedback\": \"It seems you're experiencing some conflicting feelings.  While you're excited about working out, you also seem to be struggling with your diet. Would you like some advice or resources to help balance your healthy habits?\"\n  }\n}\n```",
        f"input: {journal_entries}",
        "output: ",
        ])
    
    # Remove the triple backticks and JSON block declaration
    cleaned_resp = response.text.strip("```json\n").strip("```")

    # Convert the cleaned string into a Python dictionary
    real_dict = json.loads(cleaned_resp)

    # Print the resulting dictionary
    return real_dict 