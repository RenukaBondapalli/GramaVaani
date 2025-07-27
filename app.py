import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from io import BytesIO

# Constants
DATA_FILE = "submissions.json"
EXCEL_FILE = "submissions.xlsx"
CSV_FILE = "submissions.csv"

# Initialize data file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

# Load existing data
def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Save new data
def save_data(entry):
    data = load_data()
    data.append(entry)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Also write to Excel and CSV
    df = pd.DataFrame(data)
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')

# UI CONFIG
st.set_page_config(page_title="తెలుగు సామెతలు", layout="wide", page_icon="📜")

st.markdown("""
    <style>
        /* App Background */
        .stApp {
            background: linear-gradient(135deg, #f4f0e6 0%, #e9e0d4 100%) !important;
            font-family: 'Poppins', sans-serif;
            color: #2b2b2b;
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #e4d1b9 0%, #cbb69b 100%) !important;
            color: #2b2b2b !important;
        }

        /* Titles */
        .title {
            font-size: 48px;
            text-align: center;
            color: #7b1e1e;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 22px;
            color: #4a3c3c;
            text-align: center;
            margin-bottom: 25px;
        }

        /* Label color */
        label {
            color: #2b2b2b !important;
            font-weight: 600;
        }

        /* Input fields */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div > div {
            font-size: 17px;
            background-color: #fff;
            color: #2b2b2b;
            border: 1px solid #b58d8d;
            border-radius: 6px;
            padding: 8px;
        }

        /* Button styling */
        .stButton button,
        button[kind="primary"],
        .stDownloadButton > button,
        div.stForm button {
            background-color: #6b1d1d !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-size: 16px !important;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        .stButton button:hover,
        button[kind="primary"]:hover,
        .stDownloadButton > button:hover,
        div.stForm button:hover {
            background-color: #8c2c2c !important;
        }

        /* Proverb box */
        .proverb-box {
            background: #fff;
            border-left: 6px solid #7b1e1e;
            padding: 1.2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            color: #2c1f1f;
            transition: transform 0.2s ease-in-out;
        }

        .proverb-box:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }

        /* Dropdown select styling */
        div[data-baseweb="select"] {
            background-color: #f0e5d8 !important;
            color: #000 !important;
            border-radius: 8px;
            padding: 2px;
        }

        div[data-baseweb="select"] > div {
            color: #000 !important;
            font-size: 16px;
        }

        div[data-baseweb="popover"] {
            background-color: #fff8ef !important;
            color: #000 !important;
        }

        /* Dropdown arrow icon */
        svg {
            fill: #6b1d1d !important;
        }
        .custom-confirm {
        background-color: #d4b2a7;
        color: #3b0d0d;
        padding: 10px 16px;
        border-left: 6px solid #6b1d1d;
        border-radius: 8px;
        font-weight: 700;
        margin-top: 20px;
    }

    </style>
""", unsafe_allow_html=True)



st.markdown('<div class="title">📜 తెలుగు సామెతల సేకరణ</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="subtitle">మీ ఊరిలో ప్రసిద్ధమైన, మీరు వినే సామెతను క్రింది రూపంలో నమోదు చేయండి. వివరణ, వాడుక, ఉద్భవ స్థలం కూడా తెలపండి.</div>
""", unsafe_allow_html=True)

# Submission form
with st.form("submit_proverb", clear_on_submit=True):
    name = st.text_input("👤 Name")
    place = st.text_input("📍 Place")
    language = st.selectbox("🗣️ Language", ["Telugu", "Other"])
    proverb = st.text_area("💬 Proverb", height=100)
    explanation = st.text_area("📖 Explanation", height=100)
    category = st.selectbox("📚 Category", ["Moral", "Humor", "Wisdom", "Nature", "Other"])
    submitted = st.form_submit_button("✅ Submit Proverb")

    if submitted and name and place and proverb:
        entry = {
            "name": name,
            "place": place,
            "language": language,
            "proverb": proverb,
            "explanation": explanation,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        save_data(entry)
        st.markdown("""
    <div class="custom-confirm">
        ✅ Submitted the proverb successfully!
    </div>
""", unsafe_allow_html=True)

    elif submitted:
        st.warning("Please fill in at least Name, Place, and Proverb.")

st.markdown("---")

# Display submitted proverbs
st.subheader("📜 Submitted Proverbs")
data = load_data()

# Filter sidebar
with st.sidebar:
    st.header("🔍 Filters")
    selected_category = st.selectbox("Category", ["All"] + sorted(set(d.get("category", "Other") for d in data)))
    keyword = st.text_input("Search keyword")

filtered = []
for d in data:
    if (selected_category == "All" or d.get("category") == selected_category):
        if keyword.lower() in d.get("proverb", "").lower() or keyword.lower() in d.get("explanation", "").lower():
            filtered.append(d)

if filtered:
    for entry in reversed(filtered):
        st.markdown(f"""
        <div class='proverb-box'>
            <b>💬 Proverb:</b> {entry['proverb']}<br>
            <b>📖 Explanation:</b> {entry['explanation']}<br>
            <b>📚 Category:</b> {entry['category']}<br>
            <b>🗣️ Language:</b> {entry['language']}<br>
            <b>👤 Name:</b> {entry['name']}<br>
            <b>📍 Place:</b> {entry['place']}<br>
            <b>🕒 Timestamp:</b> {entry['timestamp'][:19].replace('T', ' ')}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No proverbs found for the selected filters.")

# Download CSV
with open(CSV_FILE, 'rb') as f:
    st.download_button("📥 Download All as CSV", data=f, file_name="telugu_proverbs.csv", mime="text/csv")
