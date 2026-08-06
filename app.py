import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Road Trip Route Generator",
    page_icon="🚗",
    layout="centered"
)

# ---------------- GET API KEY ----------------
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Groq API key not found. Please add GROQ_API_KEY to your .env file.")
    st.stop()

# ---------------- GROQ CLIENT ----------------
client = Groq(api_key=api_key)

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:40px;
    font-weight:700;
    margin-bottom:10px;
}

.subtitle {
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.card {
    padding:20px;
    border-radius:12px;
    background:#f5f7fb;
    border:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚗 AI Road Trip Route Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate smart road trip routes with stops, travel time and tips</div>', unsafe_allow_html=True)

# ---------------- INPUT FORM ----------------
with st.container():

    st.markdown('<div class="card">', unsafe_allow_html=True)

    start_city = st.text_input("Start City")
    destination = st.text_input("Destination")

    preference = st.selectbox(
        "Travel Preference",
        ["Fastest", "Scenic", "Budget"]
    )

    generate = st.button("Generate Trip Plan")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- GENERATION FUNCTION ----------------
def generate_trip(start_city, destination, preference):

    prompt = f"""
You are a travel planner.

Create a road trip travel plan.

Start city: {start_city}
Destination: {destination}
Travel preference: {preference}

Provide:
1. Best route
2. Estimated travel time
3. Three interesting stops
4. Food recommendations
5. Travel tips
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error generating trip plan: {str(e)}"


# ---------------- GENERATE BUTTON ----------------
if generate:

    if not start_city or not destination:
        st.warning("⚠️ Please enter both start city and destination.")

    else:
        with st.spinner("Generating your trip plan..."):

            result = generate_trip(start_city, destination, preference)

        st.markdown("### 🗺️ Generated Travel Plan")
        st.write(result)