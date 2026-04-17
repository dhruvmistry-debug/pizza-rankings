import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Pie Chart - Pizza Rankings", layout="centered")
ALLOWED_EMAILS = ["dhruv.mistry@gmail.com", "pran25@hotmail.co.uk"] # Update these!

# The CSV export link of your Google Sheet
# To get this: Take your sheet link and change everything after /edit... to /export?format=csv
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1ni2YaFbJv86Mz0TaGqYxlTf0fn3jJSVk49b30rRUDlI/export?format=csv"

# --- AUTH ---
user_email = st.text_input("Enter your email:")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    st.title("🍕 Pie Chart - Pizza Rankings")

    # --- INPUT FORM ---
    with st.expander("➕ Log a New Pizza", expanded=True):
        # We'll use a standard Google Form link or a simplified Save button
        # For now, let's keep the UI but we will use a different save logic
        st.info("To save data permanently, we'll use a direct link to the sheet below.")
        
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
        
        if st.button("Generate Log Entry"):
            st.code(f"{name}, {pizza}, {avg}, {'✅ YES' if avg > 8 else '❌ NO'}")
            st.success("Entry ready! Tap the 'Open Sheet' button below to paste it at the bottom.")
            st.link_button("📂 Open Google Sheet to Paste", "https://docs.google.com/spreadsheets/d/1ni2YaFbJv86Mz0TaGqYxlTf0fn3jJSVk49b30rRUDlI/edit")

    # --- LEADERBOARD ---
    st.header("🏆 The Official Leaderboard")
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        st.dataframe(df, use_container_width=True)
    except:
        st.write("Click 'Open Sheet' to add your first pizza!")

else:
    if user_email:
        st.warning("Access denied.")
