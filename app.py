import streamlit as st
import pandas as pd

st.set_page_config(page_title="Technical Assessment", layout="centered")

# Your Sheet ID from the URL you provided
SHEET_ID = "1Wn63o_7wBJLcp0GTyh6xvP4Phu7nQIzqVYtAXrYp_Zw"
# This URL format forces Google to give the data directly to the app
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Questions"

st.title("🛡️ Technical Systems Evaluation")

try:
    # Load data directly using Pandas
    df = pd.read_csv(SHEET_URL)
    
    if not df.empty:
        # Filter out any completely empty rows
        df = df.dropna(subset=['Question'])
        
        # Pull 5 random questions from each category
        categories = df['Category'].unique()
        test_questions = []
        for cat in categories:
            sample_size = min(5, len(df[df['Category'] == cat]))
            test_questions.append(df[df['Category'] == cat].sample(sample_size))
        
        test_pool = pd.concat(test_questions).reset_index(drop=True)

        with st.form("exam"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            
            responses = []
            for i, row in test_pool.iterrows():
                st.write(f"### Q{i+1}: {row['Question']}")
                # Ensure options are strings and remove NaN
                options = [str(row['A']), str(row['B']), str(row['C']), str(row['D'])]
                ans = st.radio(f"Select for Q{i+1}", options, key=f"q{i}", label_visibility="collapsed")
                responses.append(ans)
            
            if st.form_submit_button("Submit"):
                if name and email:
                    score = sum(1 for i, row in test_pool.iterrows() if str(responses[i]) == str(row['Correct']))
                    st.balloons()
                    st.success(f"Done! {name}, your score is {score}/{len(test_pool)} ({(score/len(test_pool))*100:.0f}%)")
                    st.info("Results have been displayed. Screenshot this page for your records.")
                else:
                    st.warning("Please enter your Name and Email.")

except Exception as e:
    st.error("Could not load questions. Check your Google Sheet 'Share' settings.")
    st.write(f"Error Details: {e}")
