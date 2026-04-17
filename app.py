import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Pie Chart - Pizza Rankings", layout="centered")
ALLOWED_EMAILS = ["your_email@gmail.com", "friend_email@gmail.com"]

# --- AUTH ---
user_email = st.text_input("Enter your email:")

if user_email.lower() in [e.lower() for e in ALLOWED_EMAILS]:
    # Connect to Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Read existing data
    df = conn.read()

    st.title("🍕 Pie Chart - Pizza Rankings")

    # --- INPUT FORM ---
    with st.expander("➕ Log a New Pizza", expanded=True):
        with st.form("pizza_form"):
            name = st.text_input("Restaurant Name")
            pizza = st.text_input("Pizza Name/Type")
            loc = st.text_input("Location")
            
            col1, col2 = st.columns(2)
            with col1:
                crust = st.slider("Crust (Flop?)", 0, 10, 5)
                sauce = st.slider("Sauce", 0, 10, 5)
                ingred = st.slider("Ingredients", 0, 10, 5)
            with col2:
                portion = st.slider("Portion Size", 0, 10, 5)
                price = st.slider("Price Value", 0, 10, 5)
            
            submit = st.form_submit_button("Save to Leaderboard")

            if submit:
                # Math logic
                avg = (crust + sauce + ingred + portion + price) / 5
                rec = "✅ YES" if avg > 8 else "❌ NO"
                
                # Create new row
                new_data = pd.DataFrame([{
                    "Restaurant": name, "Pizza": pizza, "Location": loc,
                    "Crust": crust, "Sauce": sauce, "Ingredients": ingred,
                    "Portion": portion, "Price": price, "Average": avg, "Recommend": rec
                }])
                
                # Update Google Sheet
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"Log Saved! Score: {avg}")

    # --- LEADERBOARD ---
    st.header("🏆 The Official Leaderboard")
    if not df.empty:
        leaderboard = df.sort_values(by="Average", ascending=False)
        st.dataframe(leaderboard[["Restaurant", "Pizza", "Average", "Recommend"]], use_container_width=True)
    else:
        st.write("No rankings yet. Start eating!")

else:
    if user_email:
        st.warning("Access denied. Please check your email or contact the admin.")
