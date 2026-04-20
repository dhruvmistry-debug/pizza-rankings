import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Pie Chart - Pizza Rankings", layout="centered")
ALLOWED_EMAILS = ["dhruv.mistry@gmail.com", "pran25@hotmail.co.uk"]

# --- GOOGLE SHEETS CONNECTION ---
# This creates a connection object using your secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- AUTH ---
user_email = st.text_input("Enter your email:")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    st.title("🍕 Pie Chart - Pizza Rankings")

    # --- INPUT FORM ---
    with st.expander("➕ Log a New Pizza", expanded=True):
        name = st.text_input("Restaurant Name")
        pizza = st.text_input("Pizza Name/Type")
        
        col1, col2 = st.columns(2)
        with col1:
            crust = st.slider("Crust", 0, 10, 5)
            sauce = st.slider("Sauce", 0, 10, 5)
        with col2:
            portion = st.slider("Portion", 0, 10, 5)
            price = st.slider("Price", 0, 10, 5)
        
        avg = (crust + sauce + portion + price) / 4
        
        if st.button("Save to Leaderboard"):
            if name and pizza:
                # 1. Fetch existing data
                existing_data = conn.read(ttl=0) # ttl=0 ensures we get fresh data
                
                # 2. Create new row
                new_entry = pd.DataFrame([{
                    "Restaurant": name,
                    "Pizza": pizza,
                    "Average Score": avg,
                    "Recommended": '✅ YES' if avg > 8 else '❌ NO'
                }])
                
                # 3. Combine and Update
                updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                conn.update(data=updated_df)
                
                st.success(f"Saved {name} to the leaderboard!")
                st.balloons()
            else:
                st.error("Please enter a name and pizza type.")

    # --- LEADERBOARD ---
    st.header("🏆 The Official Leaderboard")
    
    # Read fresh data
    df = conn.read(ttl=0)
    
    if not df.empty:
        # Sort by Average Score and add Rank
        df = df.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        df.index = df.index + 1 # Start ranking at 1 instead of 0
        df.index.name = "Rank"
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No rankings yet. Be the first to log a pizza!")

else:
    if user_email:
        st.warning("Access denied.")
