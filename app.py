import streamlit as st
import datetime
from openai import OpenAI

# ==========================
# 🔑 Direct API Key Setup
# ==========================
API_KEY = "your_api_key_here"  # Replace with your actual OpenAI API key
client = OpenAI(api_key=API_KEY)

# Page setup
st.set_page_config(page_title="Student AI Travel Planner", page_icon="🎒")
st.title("🎒 Student AI Travel Planner")

# Inputs
destination = st.text_input("Destination", placeholder="e.g., Dubai")
start_date = st.date_input("Start date", datetime.date.today())
duration = st.number_input("Duration (days)", min_value=1, max_value=15, value=3)
budget = st.selectbox("Budget level", ["tight", "moderate", "luxury"])
transport = st.selectbox("Preferred transport", ["bus/train", "flight", "bike", "car"])
stay = st.text_input("Preferred stay", placeholder="e.g., hostel, hotel, Airbnb")
interests = st.text_input("Interests (comma-separated)", placeholder="e.g., food, monuments, shopping, beach")

# Generate button
if st.button("Generate Itinerary"):
    if not destination:
        st.warning("Please enter a destination to generate your travel plan.")
    else:
        st.info("🧠 Generating your AI travel plan... please wait a few seconds.")

        # Combined prompt to reduce API calls
        combined_prompt = f"""
        You are a student travel planner. 

        1. List 5 must-visit attractions in {destination.title()} for students interested in {interests}. Return only names as bullet points.
        2. Create a short 3-paragraph trip summary for a student visiting {destination.title()}.
           Include: duration {duration} days, budget {budget}, transport {transport}, stay {stay}, interests {interests}.
        3. Create a {duration}-day itinerary using the attractions listed above. Write one short paragraph per day with 2-3 activities.

        Present the output in 3 sections:
        - Attractions
        - Trip Summary
        - Day-wise Itinerary
        """

        # API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": combined_prompt}]
        )

        result_text = response.choices[0].message.content

        # Display output
        st.markdown(result_text)
        st.success("✨ Your AI travel plan is ready! Enjoy your trip!")