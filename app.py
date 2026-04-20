import streamlit as st
import pandas as pd
import os

# --- CONFIG & STYLING ---
st.set_page_config(page_title="PIE CHART - PIZZA", layout="centered")

# Custom CSS for the 90s Hip-Hop Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');

    /* Background Stencil Effect */
    .main {
        background-color: #1a1a1a;
        background-image: url("https://www.transparenttextures.com/patterns/stardust.png"), 
                          url("https://img.icons8.com/ios/100/ffffff/pizza-slice.png");
        background-repeat: repeat, space;
        background-size: auto, 150px;
        opacity: 0.9;
    }

    /* Graffiti Style Headers */
    h1, h2, h3 {
        font-family: 'Permanent Marker', cursive !important;
        color: #FFD700 !important; /* Gold */
        text-shadow: 3px 3px #FF00FF, 6px 6px #00FFFF; /* Neon Pink & Cyan */
        letter-spacing: 2px;
        transform: rotate(-1deg);
    }

    /* Funky Card Look for Form */
    .stExpander {
        border: 3px solid #00FFFF !important;
        background-color: rgba(0,0,0,0.8) !important;
        border-radius: 15px !important;
    }

    /* Custom Button */
    div.stButton > button:first-child {
        background-color: #FF00FF;
        color: white;
        font-family: 'Permanent Marker', serif;
        font-size: 20px;
        border-radius: 0px;
        border: 2px solid #00FFFF;
        transition: 0.3s;
    }
    
    div.stButton > button:first-child:hover {
        transform: scale(1.1) rotate(2deg);
        background-color: #00FFFF;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "pizza_data.csv"
ALLOWED_EMAILS = ["dhruv.mistry@gmail.com", "pran25@hotmail.co.uk"]

# --- DATA ENGINE ---
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=[
        "Restaurant", "Pizza Ordered", "Location", 
        "Crust", "Sauce", "Quality", "Portion", "Price", 
        "
