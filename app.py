import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIG & STYLING ---
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
        background: #FF4500; color: white; font-family: 'Bangers', cursive; font-size: 24px;
        border: 2px solid #FFD700; border-radius: 0px; width: 100%; box-shadow: 5px 5px 0px #555;
    }
    div.stButton > button:first-child:hover { background: #FFD700; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
# Using the standard connection method now that the Secrets are in literal string format
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Connection failed. Please check your Secrets box formatting.")
    st.stop()

ALLOWED_EMAILS = ["dhruv.mistry@gmail.com", "pran25@hotmail.co.uk"]

# --- APP CONTENT ---
st.markdown("<h1>The Pie Chart</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #BBB; font-family: Permanent Marker; font-size: 1.5rem; margin-top: -20px;'>The only Official Unofficial Pizza Ranking</p>", unsafe_allow_html=True)

user_email = st.text_input("🔑 DROP YOUR CREDENTIALS (Email):")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    
    # Read existing data
    df = conn.read(ttl=0)

    # --- LOG ENTRY ---
    with st.expander("🍕 LOG A NEW ENTRY", expanded=False):
        with st.form("pizza_form", clear_on_submit=True):
            name = st.text_input("RESTAURANT")
            pizza = st.text_input("THE SLICE")
            loc = st.text_input("THE BLOCK (Location)")
            
            st.markdown("### THE SCORECARD")
            c1, c2 = st.columns(2)
            with c1:
                crust = st.slider("Crust (Flop vs Hold)", 0, 10, 5)
                sauce = st.slider("Sauce (Quality)", 0, 10, 5)
                quality = st.slider("Ingredients", 0, 10, 5)
            with c2:
                portion = st.slider("Portion", 0, 10, 5)
                price = st.slider("Value", 0, 10, 5)
            
            submit = st.form_submit_button("LOCK IT IN")

            if submit:
                if name and pizza:
                    avg = (crust+sauce+quality+portion+price)/5
                    new_row = pd.DataFrame([{
                        "Restaurant": name, "Pizza Ordered": pizza, "Location": loc,
                        "Crust": crust, "Sauce": sauce, "Quality": quality,
                        "Portion": portion, "Price": price,
                        "Average Score": round(avg, 2),
                        "Recommend?": "LEGIT ✅" if avg >= 8 else "WHACK ❌"
                    }])
                    
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("Restaurant and Slice name are required!")

    # --- LEADERBOARD ---
    st.markdown("<h2>PIE CHART Leaderboard</h2>", unsafe_allow_html=True)
    if not df.empty:
        # Sort and clean up display
        leaderboard = df.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        leaderboard.index += 1
        st.dataframe(leaderboard, use_container_width=True)
        
        # --- SPIN THE PIE ---
        st.markdown("---")
        st.markdown("<h2>CANT DECIDE? SPIN THE PIE!</h2>", unsafe_allow_html=True)
        
        locations = df["Location"].dropna().unique().tolist()
        col1, col2 = st.columns([1, 2])
        with col1:
            selected_loc = st.selectbox("WHERE ARE YOU?", ["Everywhere"] + locations)
        with col2:
            st.write(" ")
            if st.button("🎰 SPIN FOR A SLICE"):
                pool = df if selected_loc == "Everywhere" else df[df["Location"] == selected_loc]
                if not pool.empty:
                    choice = pool.sample(n=1).iloc[0]
                    st.markdown(f"""
                        <div style="background: #FFD700; padding: 20px; border: 5px solid #FF4500; text-align: center; box-shadow: 10px 10px 0px #333;">
                            <h3 style="color: black; font-family: 'Bangers'; margin: 0;">COWABUNGA! GO TO:</h3>
                            <h1 style="color: #FF4500; font-family: 'Permanent Marker'; font-size: 3.5rem; margin: 10px 0;">{choice['Restaurant']}</h1>
                            <p style="color: black; font-weight: bold; font-size: 1.2rem;">Try the: {choice['Pizza Ordered']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
    else:
        st.info("The wall is empty. Feed the database.")

else:
    if user_email:
        st.error("Access Denied. Email not on official reviewer list.")
