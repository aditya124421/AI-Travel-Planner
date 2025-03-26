import streamlit as st
import google.generativeai as genai

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyBHETZ4euiKNwPlwlOCcX9juwuHQ_yBKak")
MODEL_NAME = "gemini-1.5-pro-latest"

# Define conversation steps
steps = [
    "Where are you traveling from and to?",  # Step 1: Destination & Starting Location
    "How long is your trip? (e.g., 5 days, 1 week)",  # Step 2: Trip Duration
    "What's your budget? (Low, Medium, High)",  # Step 3: Budget
    "What's the purpose of your trip? (Leisure, Business, Honeymoon, Adventure, etc.)",  # Step 4: Purpose
    "What are your preferences? (Nature, Shopping, Food, History, Relaxation, etc.)",  # Step 5: Preferences
    "Do you have any dietary preferences or mobility concerns?",  # Step 6: Additional preferences
]

# ✅ Initialize session state for conversation flow
if "conversation_step" not in st.session_state:
    st.session_state.conversation_step = 0
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = []

# ✅ Function to generate AI itinerary response
def get_itinerary(user_inputs):
    model = genai.GenerativeModel(MODEL_NAME)

    # ✅ Ensure the list has exactly 6 elements (fill missing ones with "N/A")
    inputs = user_inputs + ["N/A"] * (6 - len(user_inputs))

    prompt = f"""
    You are an AI travel planner. Based on the following user inputs, create a personalized day-by-day itinerary:

    - **From:** {inputs[0]}
    - **To:** {inputs[1]}
    - **Duration:** {inputs[2]}
    - **Budget:** {inputs[3]}
    - **Purpose:** {inputs[4]}
    - **Preferences:** {inputs[5]}

    Generate a structured travel itinerary with detailed activity recommendations, including must-visit places, food spots, and estimated travel times.
    """

    response = model.generate_content(prompt)
    return response.text  # Extract text response

# ✅ UI Header
st.title("🌍 AI Travel Planner Chatbot")
st.write("Let's plan your perfect trip step by step!")

# ✅ Show previous messages
for idx, (question, answer) in enumerate(zip(steps, st.session_state.user_inputs)):
    st.write(f"**🧑 You:** {answer}")
    if idx + 1 < len(steps):
        st.write(f"**🤖 AI:** Got it! {steps[idx+1]}")

# ✅ Ask next question in sequence
if st.session_state.conversation_step < len(steps):
    user_input = st.chat_input(steps[st.session_state.conversation_step])

    if user_input:
        st.session_state.user_inputs.append(user_input)
        st.session_state.conversation_step += 1
        st.rerun()

# ✅ Ensure we have all inputs before generating itinerary
if st.session_state.conversation_step == len(steps) and len(st.session_state.user_inputs) >= 6:
    st.subheader("📅 Your Personalized Itinerary:")
    itinerary = get_itinerary(st.session_state.user_inputs)
    st.write(itinerary)