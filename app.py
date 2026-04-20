import streamlit as st
import pandas as pd
import os

# --- CONFIG & STYLING ---
st.set_page_config(page_title="The Pie Chart", layout="wide")

# Custom CSS for the NYC / 90s / Character Background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Bangers&display=swap');

    /* The Main Background Container */
    .stApp {
        background-color: #121212;
        background-image: 
            /* Spiderman Watermark */
            url("https://img.icons8.com/color/200/spiderman-old.png"),
            /* TMNT / Turtle Watermark */
            url("https://img.icons8.com/color/150/ninja-turtle.png"),
            /* Pizza Watermark */
            url("https://img.icons8.com/officel/120/pizza.png");
        background-attachment: fixed;
        background-position: top 10% left 5%, bottom 10% right 5%, center right 15%;
        background-repeat: no-repeat;
        background-blend-mode: overlay;
    }

    /* Michael Scott / Office Vibe Quote Placeholder Area */
    .main::before {
        content: "'UN-OFFICIAL' - Michael Scott";
        position: fixed;
        bottom: 20px;
        left: 20px;
        font-family: 'Courier New', monospace;
        color: rgba(255,255,255,0.2);
        font-size: 14px;
        z-index: 0;
    }

    /* Graffiti Style Headers */
    h1 {
        font-family: 'Bangers', cursive !important;
        color: #FF4500 !important; /* Pizza Sauce Red */
        text-shadow: 4px 4px #FFD700; /* Cheese Gold Shadow */
        font-size: 4rem !important;
        text-align: center;
    }

    h2 {
        font-family: 'Permanent Marker', cursive !important;
        color: #00FF00 !important; /* Turtle Green */
        text-shadow: 2px 2px #000;
        text-align: center;
    }

    /* Funky Card Look for Form */
    .stExpander {
        border: 4px solid #1E90FF !important; /* Yankees Blue */
        background-color: rgba(0,0,0,0.85) !important;
        border-radius: 20px !important;
        box-shadow: 0px 0px 20px #1E90FF;
    }

    /* Custom Button - "Post to the Wall" */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #FF4500, #FFD700);
        color: black;
        font-family: 'Bangers', cursive;
        font-size: 24px;
        border-radius: 50px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    
    div.stButton > button:first-child:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #FFD700;
    }

    /* Table Styling */
    .stDataFrame {
        border: 2px solid #FFD700;
        border-radius: 10px;
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
st.markdown("<h3 style='text-align: center; color: white; font-family: Permanent Marker;'>The only Official Unofficial Pizza Ranking</h3>", unsafe_allow_html=True)

user_email = st.text_input("🍕 ENTER THE VIP LOUNGE (Email):")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    
    with st.expander("📝 LOG YOUR SLICE", expanded=False):
        with st.form("pizza_entry", clear_on_submit=True):
            name = st.text_input("RESTAURANT NAME")
            pizza = st.text_input("WHAT SLICE DID YOU GET?")
            loc = st.text_input("LOCATION / NEIGHBORHOOD")
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                crust = st.slider("Crust (Crunch/Flavor)", 0, 10, 5)
                sauce = st.slider("Sauce (Tang/Zing)", 0, 10, 5)
                quality = st.slider("Cheese/Toppings Quality", 0, 10, 5)
            with c2:
                portion = st.slider("Slice Size/Portion", 0, 10, 5)
                price = st.slider("Price (Value for Money)", 0, 10, 5)
            
            submit = st.form_submit_button("SUBMIT TO THE ARCHIVES")

            if submit:
                if name and pizza:
                    avg = (crust + sauce + quality + portion + price) / 5
                    rec = "COWABUNGA! ✅" if avg >= 8.0 else "MEH... ❌"
                    
                    new_row = pd.DataFrame([{
                        "Restaurant": name, "Pizza Ordered": pizza, "Location": loc,
                        "Crust": crust, "Sauce": sauce, "Quality": quality,
                        "Portion": portion, "Price": price,
                        "Average Score": round(avg, 2), "Recommend?": rec
                    }])
                    
                    df = load_data()
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.balloons()
                    st.rerun()

    # --- LEADERBOARD ---
    st.markdown("<h2>PIE CHART Leaderboard</h2>", unsafe_allow_html=True)
    df = load_data()
    
    if not df.empty:
        # Sort and clean up
        leaderboard = df.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        leaderboard.index += 1
        leaderboard.index.name = "Rank"
        st.dataframe(leaderboard, use_container_width=True)
    else:
        st.info("The leaderboard is waiting for its first hero.")

else:
    if user_email:
        st.error("You aren't on the list. No pizza for you!")
