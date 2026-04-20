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
        "Average Score", "Recommend?"
    ])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# --- APP CONTENT ---
user_email = st.text_input("🎧 DROP YOUR EMAIL TO TAG A PIZZA:")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    st.title("🍕 PIE CHART: THE STREETS ARE WATCHIN'")

    with st.expander("🔥 TAG A NEW PIZZA", expanded=True):
        with st.form("pizza_entry", clear_on_submit=True):
            name = st.text_input("RESTAURANT")
            pizza = st.text_input("PIZZA TYPE")
            loc = st.text_input("LOCATION (BLOCK/CITY)")
            
            st.markdown("### THE STATS")
            col1, col2 = st.columns(2)
            with col1:
                crust = st.slider("CRUST", 0, 10, 5)
                sauce = st.slider("SAUCE", 0, 10, 5)
                quality = st.slider("QUALITY", 0, 10, 5)
            with col2:
                portion = st.slider("PORTION", 0, 10, 5)
                price = st.slider("PRICE", 0, 10, 5)
            
            submit = st.form_submit_button("POST TO THE WALL")

            if submit:
                if name and pizza:
                    avg = (crust + sauce + quality + portion + price) / 5
                    rec = "LEGENDARY ✅" if avg >= 7.5 else "WHACK ❌"
                    
                    new_row = pd.DataFrame([{
                        "Restaurant": name, "Pizza Ordered": pizza, "Location": loc,
                        "Crust": crust, "Sauce": sauce, "Quality": quality,
                        "Portion": portion, "Price": price,
                        "Average Score": round(avg, 2), "Recommend?": rec
                    }])
                    
                    df = load_data()
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.success("STENCIL APPLIED! REFRESHING...")
                else:
                    st.error("YO, FILL OUT THE NAME AND PIZZA!")

    # --- LEADERBOARD ---
    st.header("🏆 THE TOP DOGS")
    df = load_data()
    
    if not df.empty:
        leaderboard = df.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        leaderboard.index += 1
        st.dataframe(leaderboard, use_container_width=True)
    else:
        st.info("NO TAGS ON THE WALL YET.")

else:
    if user_email:
        st.warning("YOU AIN'T ON THE LIST, HOMIE.")
