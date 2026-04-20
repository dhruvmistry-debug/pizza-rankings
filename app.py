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
    conn = st.connection("gsheets", type=GSheetsConnection)

    # --- INPUT FORM ---
    with st.expander("➕ Log a New Pizza", expanded=True):
        name = st.text_input("Restaurant Name")
        pizza = st.text_input("Pizza Ordered")
        location = st.text_input("Location")
        
        col1, col2 = st.columns(2)
        with col1:
            crust = st.slider("Crust (0-10)", 0, 10, 5)
            sauce = st.slider("Sauce (0-10)", 0, 10, 5)
            quality = st.slider("Ingredient quality (0-10)", 0, 10, 5)
        with col2:
            portion = st.slider("Portion (0-10)", 0, 10, 5)
            price = st.slider("Price (0-10)", 0, 10, 5)
        
        # Calculate average based on the 5 specific categories in your sheet
        avg = (crust + sauce + quality + portion + price) / 5
        
        if st.button("Save to Leaderboard"):
            if name and pizza:
                # Get current data
                df = conn.read(ttl=0)
                
                # Create new row matching your sheet's exact column names
                new_row = pd.DataFrame([{
                    "Restaurant": name,
                    "Pizza Ordered": pizza,
                    "Location": location,
                    "Crust (0-10)": crust,
                    "Sauce (0-10)": sauce,
                    "Ingredient quality (0-10)": quality,
                    "Portion (0-10)": portion,
                    "Price (0-10)": price,
                    "Average Score": round(avg, 1),
                    "Recommend?": 'Must Try' if avg > 8 else 'Dont Bother'
                }])
                
                # Add to existing data and update
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                
                st.cache_data.clear() 
                st.success(f"Added {name} to the rankings!")
                st.rerun() 
            else:
                st.error("Please enter the Restaurant and Pizza name.")

    # --- LEADERBOARD ---
    st.header("🏆 The Official Leaderboard")
    
    # Load data
    data = conn.read(ttl=0)
    
    if not data.empty:
        # Sort by Average Score and add Rank
        leaderboard = data.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        leaderboard.index += 1
        leaderboard.index.name = "Rank"
        
        # Display only the main columns for the leaderboard view
        st.dataframe(leaderboard[["Restaurant", "Pizza Ordered", "Average Score", "Recommend?"]], use_container_width=True)
    else:
        st.info("The leaderboard is currently empty.")

else:
    if user_email:
        st.warning("Access denied.")
