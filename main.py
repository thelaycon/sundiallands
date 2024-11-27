import streamlit as st
from streamlit_lottie import st_lottie

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from agents.sleep_analysis import analyze_sleep, get_last_days_sleep_data

# Get current suggestion
sleep_suggestion = analyze_sleep()

# App title
st.title("Personal Health Dashboard")

# Sidebar navigation
section = st.sidebar.selectbox(
    "Navigate to:", 
    ["Health Suggestions", "Sleep Analysis", "Fitness Analysis", "Journal Analysis", "Visualizations"]
)

# Health Suggestions Section
if section == "Health Suggestions":
    st.header("Current Health Suggestions")
    st.write("""
    - Get at least 7-8 hours of quality sleep each night.
    - Include 150 minutes of moderate exercise weekly.
    - Stay hydrated: drink 2-3 liters of water daily.
    - Keep a daily journal for mental clarity and reflection.
    """)

# Sleep Analysis Section
elif section == "Sleep Analysis":
    st.header("Sleep Analysis")
    
    # Highlight
    st.success(f"Highlight: {sleep_suggestion}")
 
    # Analysis
    st.write("Analyze your sleep patterns below:")

    df_sleep = get_last_days_sleep_data()
    
    st.write(df_sleep)
    avg_sleep = df_sleep['Hours Slept'].mean()
    st.write(f"Average Sleep Hours in the Last Week: {avg_sleep:.2f} hours")
    if avg_sleep < 7:
        st.warning("Your average sleep is below the recommended 7-8 hours. Try to establish a consistent bedtime.")

# Fitness Analysis Section
elif section == "Fitness Analysis":
    st.header("Fitness Analysis")
    
    # Highlight
    st.success("Highlight: Aiming for 8,000-10,000 steps daily improves cardiovascular health and endurance.")
    
    # Analysis
    st.write("Track your activity patterns:")
    fitness_data = {
        'Date': pd.date_range(start='2024-11-20', periods=7),
        'Steps Taken': [5000, 7000, 8000, 6000, 10000, 7500, 8000]
    }
    df_fitness = pd.DataFrame(fitness_data)
    st.write(df_fitness)
    total_steps = df_fitness['Steps Taken'].sum()
    st.write(f"Total Steps Taken in the Last Week: {total_steps}")
    if total_steps < 70000:
        st.warning("You are below the weekly goal of 70,000 steps. Increase daily activity to stay on track.")

# Journal Analysis Section
elif section == "Journal Analysis":
    st.header("Journal Analysis")
    
    # Highlight
    st.success("Highlight: Journaling helps manage stress and track goals. Reflect daily on progress and gratitude.")
    
    # Analysis
    st.write("Review your daily reflections:")
    st.write("""
    Example Journals:
    - 2024-11-20: "Had a productive day, walked 10,000 steps!"
    - 2024-11-21: "Felt a bit tired but managed to exercise."
    - 2024-11-22: "Focused on relaxation and self-care."
    """)

# Visualizations Section
elif section == "Visualizations":
    st.header("Visualizations")
    
    # Example 1: Sleep Analysis Graph
    st.subheader("Sleep Patterns")
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df_sleep, x='Date', y='Hours Slept', marker='o')
    plt.title("Hours of Sleep Over Time")
    plt.xlabel("Date")
    plt.ylabel("Hours Slept")
    st.pyplot(plt)
    
    # Example 2: Fitness Analysis Graph
    st.subheader("Fitness Patterns")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_fitness, x='Date', y='Steps Taken', palette='viridis')
    plt.title("Daily Steps Taken")
    plt.xlabel("Date")
    plt.ylabel("Steps Taken")
    st.pyplot(plt)
