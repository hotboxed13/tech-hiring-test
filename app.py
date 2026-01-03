import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Technical Assessment", layout="centered")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Load and Randomize Questions
df = conn.read(worksheet="Questions")
if not df.empty:
    # Pulls 5 random questions from each of your 4 categories
    test_pool = pd.concat([df[df['Category'] == cat].sample(5) for cat in df['Category'].unique()]).reset_index(drop=True)

st.title("🛡️ Technical Systems Evaluation")

with st.form("exam"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    
    responses = []
    for i, row in test_pool.iterrows():
        st.write(f"**Q{i+1}: {row['Question']}**")
        ans = st.radio(f"Select for Q{i+1}", [row['A'], row['B'], row['C'], row['D']], key=f"q{i}", label_visibility="collapsed")
        responses.append(ans)
    
    if st.form_submit_button("Submit"):
        score = sum(1 for i, row in test_pool.iterrows() if responses[i] == row['Correct'])
        res = {"Name": name, "Email": email, "Score": f"{score}/20", "Percentage": f"{(score/20)*100}%", "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}
        conn.create(worksheet="Results", data=[res])
        st.success("Submitted! Your results have been recorded.")
