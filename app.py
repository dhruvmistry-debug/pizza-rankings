import streamlit as st
import pandas as pd
import os

# --- CONFIG & STYLING ---
st.set_page_config(page_title="The Pie Chart", layout="wide")

# Custom CSS for NYC Skyline and 90s Vibes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Bangers&display=swap');

    /* Main background with NYC Silhouette */
    .stApp {
        background-color: #000000;
        background-image: 
            /* Subtle Grain Texture */
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png"),
            /* NYC Skyline Silhouette */
            url("https://www.transparenttextures.com/patterns/nyc-skyline.png");
        background-attachment: fixed;
        background-position: bottom center;
        background-repeat: repeat-x;
        background-size: auto, contain;
    }

    /* Graffiti Style Headers */
    h1 {
        font-family: 'Bangers', cursive !important;
        color: #FFD700 !important; /* Gold */
        text-shadow: 5px 5px #FF4500, -2px -2px #000; /* Sauce Red shadow */
        font-size: 5rem !important;
        text-align: center;
        margin-bottom: 0px;
    }

    h2 {
        font-family: 'Permanent Marker', cursive !important;
        color: #FFFFFF !important;
        text-shadow: 2px 2px #FF4500;
        text-align: center;
        padding-top: 20px;
    }

    /* Container Styling */
    .stExpander {
        border: 2px solid #333 !important;
        background-color: rgba(20, 20, 20, 0.9) !important;
        border-radius: 10px !important;
    }

    /* Input Labels */
    label {
        font-family: 'Permanent Marker', cursive !important;
        color: #FFD700 !important;
        font-size: 1.2rem !important;
    }

    /* Custom Button */
    div.stButton > button:first-child {
        background: #FF4500;
        color: white;
        font-family: 'Bangers', cursive;
        font-size: 24px;
        border: 2px solid #FFD700;
        border-radius: 0px;
        width: 100%;
        box-shadow: 5px 5px 0px #555;
    }
    
    div.stButton > button:first-child:hover {
        background: #FFD700;
        color: black;
        box-shadow: 2px 2px 0px #555;
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
        "Average Score", "Recommend?"
    ])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# --- APP CONTENT ---
st.markdown("<h1>The Pie Chart</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #BBB; font-family: Permanent Marker; font-size: 1.5rem; margin-top: -20px;'>The only Official Unofficial Pizza Ranking</p>", unsafe_allow_html=True)

user_email = st.text_input("🔑 DROP YOUR CREDENTIALS (Email):")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    
    with st.expander("🍕 LOG A NEW ENTRY", expanded=False):
        with st.form("pizza_entry", clear_on_submit=True):
            name = st.text_input("RESTAURANT")
            pizza = st.text_input("THE SLICE")
            loc = st.text_input("THE LOCATION")
            
            st.markdown("### SCORECARD")
            c1, c2 = st.columns(2)
            with c1:
                crust = st.slider("Crust", 0, 10, 5)
                sauce = st.slider("Sauce", 0, 10, 5)
                quality = st.slider("Quality", 0, 10, 5)
            with c2:
                portion = st.slider("Portion", 0, 10, 5)
                price = st.slider("Value", 0, 10, 5)
            
            submit = st.form_submit_button("LOCK IT IN")

            if submit:
                if name and pizza:
                    avg = (crust + sauce + quality + portion + price) / 5
                    rec = "LEGIT ✅" if avg >= 8.0 else "WHACK ❌"
                    
                    new_row = pd.DataFrame([{
                        "Restaurant": name, "Pizza Ordered": pizza, "Location": loc,
                        "Crust": crust, "Sauce": sauce, "Quality": quality,
                        "Portion": portion, "Price": price,
                        "Average Score": round(avg, 2), "Recommend?": rec
                    }])
                    
                    df = load_data()
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.toast("Ranking Saved!", icon="🍕")
                    st.rerun()

    # --- LEADERBOARD ---
    st.markdown("<h2>PIE CHART Leaderboard</h2>", unsafe_allow_html=True)
    df = load_data()
    
    if not df.empty:
        # Sort by Average Score
        leaderboard = df.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        leaderboard.index += 1
        leaderboard.index.name = "Rank"
        st.dataframe(leaderboard, use_container_width=True)
    else:
        st.info("The wall is empty. Go eat some pizza.")

else:
    if user_email:
        st.error("Access Denied. You're not on the guest list.")
