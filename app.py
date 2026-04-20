import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="The Pie Chart", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Bangers&display=swap');
    .stApp {
        background-color: #000000;
        background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png"),
                          url("https://www.transparenttextures.com/patterns/nyc-skyline.png");
        background-attachment: fixed;
        background-position: bottom center;
        background-repeat: repeat-x;
        background-size: auto, contain;
    }
    h1 { font-family: 'Bangers', cursive !important; color: #FFD700 !important; text-shadow: 5px 5px #FF4500; font-size: 5rem !important; text-align: center; margin-bottom: 0px; }
    h2 { font-family: 'Permanent Marker', cursive !important; color: #FFFFFF !important; text-shadow: 2px 2px #FF4500; text-align: center; padding-top: 20px; }
    label { font-family: 'Permanent Marker', cursive !important; color: #FFD700 !important; font-size: 1.2rem !important; }
    div.stButton > button:first-child {
        background: #FF4500; color: white; font-family: 'Bangers'; font-size: 24px;
        border: 2px solid #FFD700; border-radius: 0px; width: 100%; box-shadow: 5px 5px 0px #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE FIX FOR THE TYPEERROR ---
try:
    # Load secrets
    creds = st.secrets["connections"]["gsheets"].to_dict()
    
    # 1. Clean the RSA Key
    if "private_key" in creds:
        creds["private_key"] = creds["private_key"].replace("\\n", "\n")
    
    # 2. REMOVE THE EXTRA 'TYPE' (This fixes the TypeError)
    if "type" in creds:
        creds.pop("type")
    
    # 3. Pull out the URL and connect
    url = creds.pop("spreadsheet")
    conn = st.connection("gsheets", type=GSheetsConnection, spreadsheet=url, **creds)
    
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 3. THE APP LOGIC ---
ALLOWED_EMAILS = ["dhruv.mistry@gmail.com", "pran25@hotmail.co.uk"]

st.markdown("<h1>The Pie Chart</h1>", unsafe_allow_html=True)
user_email = st.text_input("🔑 EMAIL TO ENTER:")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    df = conn.read(ttl=0)

    with st.expander("🍕 LOG A NEW ENTRY"):
        with st.form("pizza_form", clear_on_submit=True):
            name = st.text_input("RESTAURANT")
            pizza = st.text_input("THE SLICE")
            loc = st.text_input("LOCATION")
            c1, c2 = st.columns(2)
            with c1:
                crust = st.slider("Crust", 0, 10, 5)
                sauce = st.slider("Sauce", 0, 10, 5)
            with c2:
                quality = st.slider("Quality", 0, 10, 5)
                price = st.slider("Value", 0, 10, 5)
            
            if st.form_submit_button("LOCK IT IN"):
                avg = (crust+sauce+quality+price)/4
                new_row = pd.DataFrame([{"Restaurant": name, "Pizza Ordered": pizza, "Location": loc, "Average Score": avg}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.balloons()
                st.rerun()

    st.markdown("<h2>Leaderboard</h2>", unsafe_allow_html=True)
    st.dataframe(df.sort_values(by="Average Score", ascending=False), use_container_width=True)
else:
    if user_email:
        st.error("Access Denied.")
