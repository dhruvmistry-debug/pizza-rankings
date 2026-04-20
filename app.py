import streamlit as st
import pandas as pd
import os

DB_FILE = "pizza_rankings.csv"

# Load existing data or create a blank one
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Restaurant", "Pizza", "Score"])

# --- INPUT ---
with st.form("pizza_form"):
    name = st.text_input("Restaurant")
    pizza = st.text_input("Pizza")
    score = st.slider("Score", 0, 10, 5)
    
    if st.form_submit_button("Save Entry"):
        new_entry = pd.DataFrame([{"Restaurant": name, "Pizza": pizza, "Score": score}])
        df = pd.concat([df, new_entry], ignore_index=True)
        # SAVE TO FILE
        df.to_csv(DB_FILE, index=False)
        st.success("Saved locally!")

# --- DISPLAY ---
st.header("🏆 Local Leaderboard")
st.table(df.sort_values(by="Score", ascending=False))
