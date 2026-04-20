import streamlit as st
import pandas as pd
import os

# --- CONFIG ---
st.set_page_config(page_title="Pie Chart - Pizza Rankings", layout="centered")
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

# --- AUTH ---
user_email = st.text_input("Enter your email to log a pizza:")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    st.title("🍕 Pie Chart - Pizza Rankings")

    # --- INPUT FORM ---
    with st.expander("➕ Log a New Pizza", expanded=True):
        with st.form("pizza_entry", clear_on_submit=True):
            name = st.text_input("Restaurant Name")
            pizza = st.text_input("Pizza Ordered")
            loc = st.text_input("Location")
            
            col1, col2 = st.columns(2)
            with col1:
                crust = st.slider("Crust (0-10)", 0, 10, 5)
                sauce = st.slider("Sauce (0-10)", 0, 10, 5)
                quality = st.slider("Ingredient quality (0-10)", 0, 10, 5)
            with col2:
                portion = st.slider("Portion (0-10)", 0, 10, 5)
                price = st.slider("Price (0-10)", 0, 10, 5)
            
            submit = st.form_submit_button("Submit Ranking")

            if submit:
                if name and pizza:
                    # Calculate Mean Score
                    avg = (crust + sauce + quality + portion + price) / 5
                    rec = "Must Try ✅" if avg >= 7.5 else "Don't Bother ❌"
                    
                    # Create new entry
                    new_row = pd.DataFrame([{
                        "Restaurant": name,
                        "Pizza Ordered": pizza,
                        "Location": loc,
                        "Crust": crust,
                        "Sauce": sauce,
                        "Quality": quality,
                        "Portion": portion,
                        "Price": price,
                        "Average Score": round(avg, 2),
                        "Recommend?": rec
                    }])
                    
                    # Update local file
                    df = load_data()
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.success(f"Added {name}! Refreshing leaderboard...")
                else:
                    st.error("Restaurant and Pizza name are required.")

    # --- LEADERBOARD ---
    st.header("🏆 The Official Leaderboard")
    df = load_data()
    
    if not df.empty:
        # Sort by Average Score
        leaderboard = df.sort_values(by="Average Score", ascending=False).reset_index(drop=True)
        # Add Rank column starting at 1
        leaderboard.index += 1
        leaderboard.index.name = "Rank"
        
        # Display the table
        st.dataframe(leaderboard, use_container_width=True)
    else:
        st.info("No rankings yet. Start eating!")

else:
    if user_email:
        st.warning("Access denied.")
