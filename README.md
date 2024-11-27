```markdown
# Sundial Lands Health Monitor

Welcome to the Sundial Lands Health Monitor! This project provides a suite of AI-driven agents designed to analyze and provide insights on sleep, journal sentiment, and fitness activity. These agents work with user data and provide personalized suggestions to improve overall health. The insights from all agents are integrated into one comprehensive view, which is displayed on the homepage.

## Project Setup

Follow the steps below to set up and run the project:

### 1. Install Dependencies
Ensure that you have Python installed. Then, install the required libraries by running:

```bash
pip install -r requirements.txt
```

### 2. Running the Application

To start the application, use the following Streamlit command:

```bash
streamlit run main.py
```

This will launch the project in your default web browser.

## AI Agents

The project includes three core AI agents that analyze health-related data and provide actionable insights:

### 1. **Sleep Analyzer**
   - **Functionality**: 
     - Analyzes the user’s sleep history, including sleep disturbances.
     - Uses the ARIMA model to predict sleep patterns for the next 7 days.
     - Merges the predicted data with the user’s existing sleep history.
     - Sends the merged data to a fine-tuned **Gemini model** for deeper insights into the user’s sleep quality and disturbances.

### 2. **Journal Sentiment Analyzer**
   - **Functionality**: 
     - Takes journal entries as input.
     - Sends the entries to a **pre-trained Gemini model** for sentiment analysis.
     - Provides feedback on the emotional tone and mood trends of the journal entries.

### 3. **Fitness Analyzer**
   - **Functionality**: 
     - Analyzes fitness data such as steps, active minutes, and calories burned.
     - Uses **K-means clustering** to classify activity patterns based on historical data.
     - Predicts whether current activity levels (based on the last 7 days of data) should be increased or maintained.
     - Suggests adjustments to the user’s activity level based on data and domain expertise.
     - Data is imported using a saved K-means model that is trained on past activity data.

### 4. **Insight Agent**
   - **Functionality**: 
     - Integrates insights from the **Sleep Analyzer**, **Journal Sentiment Analyzer**, and **Fitness Analyzer**.
     - Combines the individual results into a single, cohesive set of insights.
     - Displays these insights on the homepage, providing a comprehensive view of the user’s health trends and suggestions.

## Data Access

Each agent has access to a sample JSON file, which contains the user’s health data (e.g., sleep history, journal entries, and fitness metrics). This data is used for prediction, analysis, and insights generation. You can replace the sample data with real user data in the appropriate format.

## Running the Project

Once all dependencies are installed, the project is ready to run. Simply run the Streamlit app with the following command:

```bash
streamlit run main.py
```

The homepage will display the integrated insights from all agents, offering a detailed overview of the user's sleep patterns, journal sentiment, and fitness activity.

```