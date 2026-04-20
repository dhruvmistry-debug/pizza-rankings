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
    h1 { font-family: 'Bangers', cursive; color: #FFD700; text-shadow: 5px 5px #FF4500; font-size: 5rem; text-align: center; margin-bottom: 0px; }
    h2 { font-family: 'Permanent Marker', cursive; color: #FFFFFF; text-shadow: 2px 2px #FF4500; text-align: center; padding-top: 20px; }
    label { font-family: 'Permanent Marker', cursive !important; color: #FFD700 !important; font-size: 1.2rem !important; }
    
    /* Input Styling */
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; border: 1px solid #FFD700; }
    
    /* Button Styling */
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
    div.stButton > button:first-child:hover { background: #FFD700; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)
ALLOWED_EMAILS = ["dhruv.mistry@gmail.com", "pran25@hotmail.co.uk"]

# --- APP CONTENT ---
st.markdown("<h1>The Pie Chart</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #BBB; font-family: Permanent Marker; font-size: 1.5rem; margin-top: -20px;'>The only Official Unofficial Pizza Ranking</p>", unsafe_allow_html=True)

user_email = st.text_input("🔑 DROP YOUR CREDENTIALS (Email):")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    
    # 1. LOAD DATA AT THE TOP SO ALL SECTIONS CAN USE IT
    df = conn.read(ttl=0)

    with st.expander("🍕 LOG A NEW ENTRY", expanded=False):
        with st.form("pizza_entry", clear_on_submit=True):
            name = st.text_input("RESTAURANT")
            pizza = st.text_input("THE SLICE")
            loc = st.text_input("THE BLOCK (Location)")
            
            st.markdown("### THE SCORECARD")
            c1, c2 = st.columns(2)
            with c1:
                crust = st.slider("Crust - Was there any flop or did it hold?", 0, 10, 5)
                sauce = st.slider("Sauce - How was the quality of that tomato base?", 0, 10, 5)
                quality = st.slider("Ingredients - Did the toppings run the show?", 0, 10, 5)
            with c2:
                portion = st.slider("Portion - Were they generous for a NY pie?", 0, 10, 5)
                price = st.slider("Value - How badly did it set you back?", 0, 10, 5)
            
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
                    
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.toast("Ranking Saved!", icon="🍕")
                    st.rerun()

    # --- LEADERBOARD ---
    st.markdown("<h2>PIE CHART Leaderboard</h2>", unsafe_allow_html=True)
    
    if not df.empty:
        leaderboard = df.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        leaderboard.index += 1
        leaderboard.index.name = "Rank"
        st.dataframe(leaderboard, use_container_width=True)
        
        # --- SPIN THE PIE FEATURE ---
        st.markdown("---")
        st.markdown("<h2>CANT DECIDE? SPIN THE PIE!</h2>", unsafe_allow_html=True)
        
        # Filter out rows where location might be empty
        valid_locations = df.dropna(subset=["Location"])
        locations = valid_locations["Location"].unique().tolist()
        
        col_spin1, col_spin2 = st.columns([1, 2])
        
        with col_spin1:
            selected_loc = st.selectbox("WHERE ARE YOU?", ["Everywhere"] + locations)
        
        with col_spin2:
            st.write(" ")
            if st.button("🎰 SPIN FOR A SLICE"):
                if selected_loc == "Everywhere":
                    pool = df
                else:
                    pool = df[df["Location"] == selected_loc]
                
                if not pool.empty:
                    choice = pool.sample(n=1).iloc[0]
                    st.markdown(f"""
                        <div style="background: #FFD700; padding: 20px; border-radius: 0px; border: 5px solid #FF4500; text-align: center; box-shadow: 10px 10px 0px #333;">
                            <h3 style="color: black; font-family: 'Bangers'; margin: 0;">COWABUNGA! GO TO:</h3>
                            <h1 style="color: #FF4500; font-family: 'Permanent Marker'; font-size: 3rem; margin: 10px 0;">{choice['Restaurant']}</h1>
                            <p style="color: black; font-family: 'Permanent Marker'; font-size: 1.2rem;">Try the: {choice['Pizza Ordered']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
    else:
        st.info("The wall is empty. Go eat some pizza.")

else:
    if user_email:
        st.error("Access Denied. You're not on the guest list.")
