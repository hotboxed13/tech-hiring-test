import streamlit as st
import pandas as pd

st.set_page_config(page_title="Technical Assessment", layout="centered")

# This is the built-in way to connect to Google Sheets
conn = st.connection("gsheets", type="spreadsheet")

# Load data from your sheet
try:
    df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1Wn63o_7wBJLcp0GTyh6xvP4Phu7nQIzqVYtAXrYp_Zw", worksheet="Questions")
    
    if not df.empty:
        # Pulls 5 random questions from each unique category found in your sheet
        test_pool = pd.concat([df[df['Category'] == cat].sample(5) for cat in df['Category'].unique()]).reset_index(drop=True)
    
    st.title("🛡️ Technical Systems Evaluation")

    with st.form("exam"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        
        responses = []
        for i, row in test_pool.iterrows():
            st.write(f"### Q{i+1}: {row['Question']}")
            ans = st.radio(f"Select for Q{i+1}", [row['A'], row['B'], row['C'], row['D']], key=f"q{i}", label_visibility="collapsed")
            responses.append(ans)
        
        if st.form_submit_button("Submit"):
            score = sum(1 for i, row in test_pool.iterrows() if responses[i] == row['Correct'])
            st.success(f"Thank you {name}, your results have been recorded. Score: {score}/20")
            # In this version, we display the score. 
            # Note: Writing back to Sheets requires your Service Account JSON in Secrets.

except Exception as e:
    st.error("Sheet Connection Error. Please ensure the Google Sheet is shared with 'Anyone with the link can edit'.")
    st.write(e)
