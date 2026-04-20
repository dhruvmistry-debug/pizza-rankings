import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# (Your funky CSS and skyline logic stays here)

conn = st.connection("gsheets", type=GSheetsConnection)

# AUTH & DATA LOADING
user_email = st.text_input("🔑 DROP YOUR CREDENTIALS:")
if user_email.lower() in ["dhruv.mistry@gmail.com", "pran25@hotmail.co.uk"]:
    
    # Read existing data
    df = conn.read(ttl=0)

    with st.expander("🍕 LOG A NEW ENTRY"):
        with st.form("pizza_form"):
            name = st.text_input("RESTAURANT")
            pizza = st.text_input("THE SLICE")
            loc = st.text_input("THE BLOCK (Location)")
            
            c1, c2 = st.columns(2)
            with c1:
                crust = st.slider("Crust - Flop or Hold?", 0, 10, 5)
                sauce = st.slider("Sauce - Quality?", 0, 10, 5)
                quality = st.slider("Ingredients - Balance?", 0, 10, 5)
            with c2:
                portion = st.slider("Portion - NY Size?", 0, 10, 5)
                price = st.slider("Value - The Damage?", 0, 10, 5)
            
            submit = st.form_submit_button("LOCK IT IN")

            if submit:
                avg = (crust+sauce+quality+portion+price)/5
                new_row = pd.DataFrame([{
                    "Restaurant": name, "Pizza Ordered": pizza, "Location": loc,
                    "Crust": crust, "Sauce": sauce, "Quality": quality,
                    "Portion": portion, "Price": price,
                    "Average Score": round(avg, 2),
                    "Recommend?": "LEGIT ✅" if avg >= 8 else "WHACK ❌"
                }])
                
                # UPDATE COMMAND (Will work now!)
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.balloons()
                st.rerun()

    # LEADERBOARD & SPIN THE PIE logic follows...
