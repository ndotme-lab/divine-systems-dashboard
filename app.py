import streamlit as st
import random
import json
from datetime import datetime

# --- Page setup ---
st.set_page_config(page_title="🌸 Divine Systems Daily Affirmation", layout="centered")

# --- Safety check & load affirmations ---
st.write("👋 App is running — loading affirmations...")
try:
    with open("affirmation_bank.json", "r", encoding="utf-8") as f:
        affirmations = json.load(f)
except Exception as e:
    st.error(f"⚠️ Could not load affirmation_bank.json: {e}")
    affirmations = [{"text": "Affirmation data not loaded.", "category": "Error"}]

# --- Custom CSS ---
st.markdown("""
    <style>
        body {
            background-color: #fff1ea;
            font-family: 'Inter', sans-serif;
        }
        .main-title {
            background-color: #152d69;
            color: white;
            padding: 0.8rem;
            border-radius: 12px;
            text-align: center;
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .sub-title {
            background-color: #f7931e;
            color: #521305;
            padding: 0.6rem;
            border-radius: 8px;
            text-align: center;
            font-size: 1.3rem;
            font-weight: 600;
        }
        .affirmation-box {
            background-color: white;
            border: 2px solid #e6f0fc;
            border-radius: 16px;
            padding: 1.2rem;
            margin-top: 1rem;
            box-shadow: 0px 3px 8px rgba(21,45,105,0.15);
            color: #521305;
            font-size: 1.2rem;
            line-height: 1.6;
        }
        .alignment-subtitle {
            font-size: 1rem;
            font-weight: 600;
            color: #152d69;
            text-align: center;
            margin-top: 1.2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='main-title'>🌸 Divine Systems Daily Affirmation</div>", unsafe_allow_html=True)

# --- Choose category ---
categories = sorted(list(set([a["category"] for a in affirmations])))
selected_category = st.selectbox("🌸 Choose a category", ["All"] + categories)

# --- Filter affirmations based on category ---
if selected_category == "All":
    filtered_affirmations = affirmations
else:
    filtered_affirmations = [a for a in affirmations if a["category"] == selected_category]

# --- Generate or show affirmation ---
if "selected_affirmation" not in st.session_state:
    st.session_state.selected_affirmation = random.choice(filtered_affirmations)

affirmation = st.session_state.selected_affirmation


# --- Display affirmation section ---
st.markdown("<div class='sub-title'>✨ Today's Affirmation</div>", unsafe_allow_html=True)
st.markdown(f"<div class='affirmation-box'>📖 {affirmation['text']}</div>", unsafe_allow_html=True)
st.write(f"🏷️ **Category:** {affirmation.get('category', 'General')}")

# --- Reflection section ---
st.markdown("<div class='alignment-subtitle'>How aligned do you feel today?</div>", unsafe_allow_html=True)
alignment = st.radio("", ["Aligned 🌿", "Integrating 🌸", "Unaligned 🌧️"])
reflection = st.text_area("🪶 Reflection (optional):")

# --- Save and refresh ---
if st.button("💾 Save & Get New Affirmation"):
    log_entry = {
        "text": affirmation["text"],
        "category": affirmation.get("category", ""),
        "alignment": alignment,
        "reflection": reflection,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("affirmation_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    st.success("🗂️ Saved to your affirmation log.")
    st.session_state.selected_affirmation = random.choice(affirmations)
    st.rerun()

st.markdown("---")
st.caption("🌸 Powered by ByThandi • Divine Systems v3")

