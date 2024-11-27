import streamlit as st
import pandas as pd
import plotly.express as px
from agents.sleep_analysis import analyze_sleep, get_last_days_sleep_data
from agents.fitness_tracking import analyze_fitness, get_last_days_fitness_data, recommend_steps

# App title
st.title("Personal Health Dashboard")

# Sidebar navigation
section = st.sidebar.selectbox(
    "Navigate to:", 
    ["Health Suggestions", "Sleep Analysis", "Fitness Analysis", "Journal Analysis"]
)

# Fetch initial data for visualizations
df_sleep = get_last_days_sleep_data()
df_fitness = get_last_days_fitness_data()

# Health Suggestions Section
if section == "Health Suggestions":
    st.header("Current Health Suggestions")
    st.write("""
    - Get at least 7-8 hours of quality sleep each night.
    - Include 150 minutes of moderate exercise weekly.
    - Stay hydrated: drink 2-3 liters of water daily.
    - Keep a daily journal for mental clarity and reflection.
    """)

    # Sleep Patterns Visualization
    if not df_sleep.empty:
        st.subheader("Sleep Patterns")
        fig_sleep = px.line(
            df_sleep, 
            x='Date', 
            y='Sleep Duration', 
            title="Hours of Sleep Over Time",
            labels={'Date': 'Date', 'Sleep Duration': 'Hours Slept'},
            markers=True
        )
        st.plotly_chart(fig_sleep)
    else:
        st.warning("No sleep data available for visualization.")

    # Fitness Patterns Visualization
    if not df_fitness.empty:
        st.subheader("Fitness Patterns")

        # Steps Taken
        fig_steps = px.bar(
            df_fitness, 
            x='Date', 
            y='Steps Taken', 
            title="Daily Steps Taken",
            labels={'Date': 'Date', 'Steps Taken': 'Steps'},
            color='Steps Taken',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_steps)

        # Calories Burned
        fig_calories = px.line(
            df_fitness, 
            x='Date', 
            y='Calories Burned', 
            title="Calories Burned Over Time",
            labels={'Date': 'Date', 'Calories Burned': 'Calories'},
            markers=True,
            line_shape='spline'
        )
        st.plotly_chart(fig_calories)
    else:
        st.warning("No fitness data available for visualization.")

# Sleep Analysis Section
elif section == "Sleep Analysis":
    sleep_suggestion = analyze_sleep()

    st.header("Sleep Analysis")
    st.success(f"Highlight: {sleep_suggestion}")
    st.write("Analyze your sleep patterns below:")

    st.write(df_sleep)
    if not df_sleep.empty:
        avg_sleep = df_sleep['Sleep Duration'].mean()
        st.write(f"Average Sleep Hours in the Last Week: {avg_sleep:.2f} hours")
        if avg_sleep < 7:
            st.warning("Your average sleep is below the recommended 7-8 hours. Try to establish a consistent bedtime.")
    else:
        st.warning("No sleep data available for analysis.")

# Fitness Analysis Section
elif section == "Fitness Analysis":
    st.header("Fitness Analysis")

    if not df_fitness.empty:
        # Summarize data
        average_steps = df_fitness["Steps Taken"].mean()
        average_calories = df_fitness["Calories Burned"].mean()
        average_active_minutes = df_fitness["Active Minutes"].mean()

        # Create user data for recommendations
        user_data = {
            "Steps": int(average_steps),
            "Calories_Burned": int(average_calories),
            "Active_Minutes": int(average_active_minutes),
        }

        # Recommendations
        recommendation_result = recommend_steps(user_data)
        fitness_suggestion = analyze_fitness(recommendation_result)

        st.success(f"Highlight: {fitness_suggestion}")
        st.write("Track your activity patterns:")
        st.write(df_fitness)

        # Fitness Insights
        total_steps = df_fitness['Steps Taken'].sum()
        total_calories = df_fitness['Calories Burned'].sum()
        st.write(f"Total Steps Taken in the Last Week: {total_steps}")
        st.write(f"Total Calories Burned in the Last Week: {total_calories:.2f} kcal")

        # Suggestions
        if total_steps < 70000:
            st.warning("You are below the weekly goal of 70,000 steps. Increase daily activity to stay on track.")
        if total_calories < 2000:  # Example threshold
            st.warning("Consider increasing your activity to burn more calories and maintain a healthy balance.")

    else:
        st.warning("No fitness data available for analysis.")

# Journal Analysis Section
elif section == "Journal Analysis":
    st.header("Journal Analysis")
    st.success("Highlight: Journaling helps manage stress and track goals. Reflect daily on progress and gratitude.")
    st.write("Review your daily reflections:")
    st.write("""
    Example Journals:
    - 2024-11-20: "Had a productive day, walked 10,000 steps!"
    - 2024-11-21: "Felt a bit tired but managed to exercise."
    - 2024-11-22: "Focused on relaxation and self-care."
    """)
