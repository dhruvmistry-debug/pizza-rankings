import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Pie Chart - Pizza Rankings", layout="centered")
ALLOWED_EMAILS = ["dhruv.mistry@gmail.com", "pran25@hotmail.co.uk"]

# --- AUTH ---
user_email = st.text_input("Enter your email:")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    st.title("🍕 Pie Chart - Pizza Rankings")

    # Connect to Google Sheets
    # Ensure your Sheet is "Anyone with the link can EDIT" for this to work easily
    conn = st.connection("gsheets", type=GSheetsConnection)

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
                # Get current data
                df = conn.read()
                
                # Create new row
                new_row = pd.DataFrame([{
                    "Restaurant": name,
                    "Pizza": pizza,
                    "Average Score": avg,
                    "Recommended": '✅ YES' if avg > 8 else '❌ NO'
                }])
                
                # Add to existing data
                updated_df = pd.concat([df, new_row], ignore_index=True)
                
                # Write back to sheet
                # IMPORTANT: This requires the sheet to be Shared as "Editor" 
                # with the email found in your Streamlit Service Account or 
                # properly configured in Secrets.
                conn.update(data=updated_df)
                
                st.cache_data.clear() # Clear cache so leaderboard updates immediately
                st.success("Pizza logged!")
                st.rerun() 
            else:
                st.error("Please fill in the names!")

    # --- LEADERBOARD ---
    st.header("🏆 The Official Leaderboard")
    
    # Load data with ttl=0 to always get the latest
    data = conn.read(ttl=0)
    
    if not data.empty:
        # Sorting and Ranking logic
        leaderboard = data.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        leaderboard.index += 1
        st.table(leaderboard) # Using st.table for a cleaner leaderboard look
    else:
        st.info("The leaderboard is currently empty.")

else:
    if user_email:
        st.warning("Access denied.")
