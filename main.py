import streamlit as st
import pandas as pd
import plotly.express as px
from agents.sleep_analysis import analyze_sleep, get_last_days_sleep_data
from agents.fitness_tracking import analyze_fitness, get_last_days_fitness_data, recommend_steps
from agents.journal_sentimental_analysis import sentimentalize, get_last_days_journal_entries
from agents.insights import get_combined_insights

# Set the custom theme
st.set_page_config(
    page_title="Personal Health Dashboard",  # Title of the web page
    page_icon="🌱",  # Icon for the tab
    layout="wide",  # Layout style
    initial_sidebar_state="expanded",  # Start sidebar expanded
)

# Inject custom CSS for enhanced design
st.markdown(
    """
    <style>
    .big-title {
        font-size: 30px;
        font-weight: bold;
        color: #4CAF50;
    }
    .sub-title {
        font-size: 20px;
        color: #FF5733;
    }
    .section-header {
        font-size: 24px;
        color: #1E90FF;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.markdown('<div class="big-title">✨ Sundial Lands ✨</div>', unsafe_allow_html=True)

# Sidebar navigation
section = st.sidebar.selectbox(
    "Navigate to:",
    ["Health Suggestions", "Sleep Analysis", "Fitness Analysis", "Journal Analysis"],
    index=0,  # Default to Health Suggestions
    key="main_nav"
)

# Fetch initial data for visualizations
df_sleep = get_last_days_sleep_data()
df_fitness = get_last_days_fitness_data()

# Function to get combined health insights
def combined_insights():
    sleep_suggestion = analyze_sleep()
    summary = sentimentalize()

    # Summarize fitness data
    avg_steps = df_fitness["Steps Taken"].mean()
    avg_calories = df_fitness["Calories Burned"].mean()
    avg_active_minutes = df_fitness["Active Minutes"].mean()

    # Create user data for recommendations
    user_data = {
        "Steps": int(avg_steps),
        "Calories_Burned": int(avg_calories),
        "Active_Minutes": int(avg_active_minutes),
    }

    # Fitness recommendations
    recommendation_result = recommend_steps(user_data)
    fitness_suggestion = analyze_fitness(recommendation_result)

    combined_info = sleep_suggestion + "\n" + summary + "\n" + fitness_suggestion
    return get_combined_insights(combined_info)

# Health Suggestions Section
if section == "Health Suggestions":
    insights = combined_insights()

    st.balloons()
    st.markdown('<div class="section-header">💡 Current Health Suggestions</div>', unsafe_allow_html=True)
    for insight in insights:
        st.markdown(f"- {insight}")

    # Sleep Data Visualization
    if not df_sleep.empty:
        df_sleep_reset = df_sleep.reset_index()

        # Sleep Pattern Visualization
        fig_sleep = px.line(
            df_sleep_reset,
            x='Date',
            y='Sleep Duration',
            title="🛌 Hours of Sleep Over Time",
            labels={'Date': 'Date', 'Sleep Duration': 'Hours Slept'},
            markers=True,
            template="plotly_dark"
        )
        st.plotly_chart(fig_sleep, use_container_width=True)
    else:
        st.warning("No sleep data available for visualization.")

    # Fitness Data Visualization
    if not df_fitness.empty:
        st.subheader("🏃‍♂️ Fitness Patterns")
        df_fitness_reset = df_fitness.reset_index()

        # Steps Taken Visualization
        fig_steps = px.bar(
            df_fitness_reset,
            x='Date',
            y='Steps Taken',
            title="🚶‍♀️ Daily Steps Taken",
            labels={'Date': 'Date', 'Steps Taken': 'Steps'},
            color='Steps Taken',
            color_continuous_scale='Viridis',
            template="plotly_dark"
        )
        st.plotly_chart(fig_steps, use_container_width=True)

        # Calories Burned Visualization
        fig_calories = px.line(
            df_fitness_reset,
            x='Date',
            y='Calories Burned',
            title="🔥 Calories Burned Over Time",
            labels={'Date': 'Date', 'Calories Burned': 'Calories'},
            markers=True,
            line_shape='spline',
            template="plotly_dark"
        )
        st.plotly_chart(fig_calories, use_container_width=True)
    else:
        st.warning("No fitness data available for visualization.")

# Sleep Analysis Section
elif section == "Sleep Analysis":
    sleep_suggestion = analyze_sleep()

    st.markdown('<div class="section-header">🛏️ Sleep Analysis</div>', unsafe_allow_html=True)
    st.success(f"✨ Highlight: {sleep_suggestion}")
    st.write("Analyze your sleep patterns below:")

    if not df_sleep.empty:
        st.write(df_sleep)
        avg_sleep = df_sleep['Sleep Duration'].mean()
        st.write(f"🕒 Average Sleep Hours in the Last Week: **{avg_sleep:.2f}** hours")
        if avg_sleep < 7:
            st.warning("⚠️ Your average sleep is below the recommended 7-8 hours. Try to establish a consistent bedtime.")
    else:
        st.warning("No sleep data available for analysis.")

# Fitness Analysis Section
elif section == "Fitness Analysis":
    st.markdown('<div class="section-header">💪 Fitness Analysis</div>', unsafe_allow_html=True)

    if not df_fitness.empty:
        # Summarize data
        avg_steps = df_fitness["Steps Taken"].mean()
        avg_calories = df_fitness["Calories Burned"].mean()
        avg_active_minutes = df_fitness["Active Minutes"].mean()

        # Create user data for recommendations
        user_data = {
            "Steps": int(avg_steps),
            "Calories_Burned": int(avg_calories),
            "Active_Minutes": int(avg_active_minutes),
        }

        # Fitness suggestions
        recommendation_result = recommend_steps(user_data)
        fitness_suggestion = analyze_fitness(recommendation_result)

        st.success(f"✨ Highlight: {fitness_suggestion}")
        st.write("Track your activity patterns:")
        st.write(df_fitness)

        # Fitness Insights
        total_steps = df_fitness['Steps Taken'].sum()
        total_calories = df_fitness['Calories Burned'].sum()
        st.write(f"🛤️ **Total Steps Taken** in the Last Week: **{total_steps}** steps")
        st.write(f"🔥 **Total Calories Burned** in the Last Week: **{total_calories:.2f}** kcal")

        # Suggestions
        if total_steps < 70000:
            st.warning("⚠️ You are below the weekly goal of 70,000 steps. Increase daily activity to stay on track.")
        if total_calories < 2000:
            st.warning("⚠️ Consider increasing your activity to burn more calories and maintain a healthy balance.")
    else:
        st.warning("No fitness data available for analysis.")

# Journal Analysis Section
elif section == "Journal Analysis":
    summary = sentimentalize()
    journal_entries = get_last_days_journal_entries()

    st.markdown('<div class="section-header">📓 Journal Analysis</div>', unsafe_allow_html=True)
    st.success(f"✨ Highlight: {summary}")

    if not journal_entries.empty:
        journal_entries_reset = journal_entries.reset_index()
        for _, row in journal_entries_reset.iterrows():
            with st.expander(f"{row['Date'].strftime('%Y-%m-%d')} Entry"):
                st.write(row['Entry'])
    else:
        st.warning("No journal entries found for the last 7 days.")
