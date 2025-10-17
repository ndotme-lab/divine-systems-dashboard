import streamlit as st
import random
import json
from datetime import datetime

# --- Page setup ---
st.set_page_config(page_title="🌸 Divine Systems Daily Affirmation", layout="centered")

# --- Safety check & load affirmation bank ---
st.write("👋 App is running — loading affirmations...")

try:
    with open("affirmation_bank.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        affirmations = data.get("affirmations", [])
except Exception as e:
    st.error(f"⚠️ Could not load affirmation_bank.json: {e}")
    affirmations = [{"text": "Affirmation data not loaded.", "category": "Error"}]

# --- Friendly display names (UI only) ---
CATEGORY_DISPLAY = {
    "Create": "Create Flow",
    "Build": "Build Discipline",
    "Believe": "Believe Again",
    "Weave": "Weave Wholeness"
}

# --- Filter affirmations to 4 canon categories only ---
affirmations = [a for a in affirmations if a.get("category") in CATEGORY_DISPLAY.keys()]

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

# --- Category selection ---
display_options = ["All"] + list(CATEGORY_DISPLAY.values())
selected_display = st.selectbox("🌸 Choose a category", display_options)

# Convert back to internal category name
if selected_display == "All":
    filtered_affirmations = affirmations
else:
    internal_category = next(k for k, v in CATEGORY_DISPLAY.items() if v == selected_display)
    filtered_affirmations = [a for a in affirmations if a["category"] == internal_category]

# --- Choose an affirmation (avoid repeating the same one twice) ---
if "last_affirmation_id" not in st.session_state:
    st.session_state.last_affirmation_id = None

new_affirmation = random.choice(filtered_affirmations)
while (
    st.session_state.last_affirmation_id is not None
    and new_affirmation["id"] == st.session_state.last_affirmation_id
    and len(filtered_affirmations) > 1
):
    new_affirmation = random.choice(filtered_affirmations)

st.session_state.selected_affirmation = new_affirmation
st.session_state.last_affirmation_id = new_affirmation["id"]
affirmation = new_affirmation

# --- Display affirmation section ---
st.markdown("<div class='sub-title'>✨ Today's Affirmation</div>", unsafe_allow_html=True)
st.markdown(f"<div class='affirmation-box'>📖 {affirmation['text']}</div>", unsafe_allow_html=True)

display_category = CATEGORY_DISPLAY.get(affirmation["category"], affirmation["category"])
st.write(f"🏷️ **Category:** {display_category}")

# --- Reflection / Alignment section ---
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
