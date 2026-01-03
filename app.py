import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Technical Skills Assessment", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stRadio > label { font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Technical Systems Evaluation")
st.subheader("Networking | CCTV | Access Control | Installation")
st.write("Complete the assessment below. Results are automatically sent to the hiring manager.")

# Connect to Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Load Questions from the 'Questions' tab
    df = conn.read(worksheet="Questions")
    
    # 1. Randomize: Pick 5 questions from each of the 4 categories
    # This ensures a unique 20-question test for every candidate
    if not df.empty:
        test_pool = pd.concat([
            df[df['Category'] == 'Networking'].sample(5),
            df[df['Category'] == 'Security'].sample(5),
            df[df['Category'] == 'CCTV'].sample(5),
            df[df['Category'] == 'Construction'].sample(5)
        ]).reset_index(drop=True)
    
    with st.form("exam_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
        with col2:
            email = st.text_input("Email Address")
        
        st.divider()
        
        # 2. Display Questions
        user_answers = []
        for i, row in test_pool.iterrows():
            st.write(f"### Question {i+1}")
            st.write(row['Question'])
            
            # If the question involves a diagram, you can add logic here to show it
            # st.image(row['Image_URL']) 
            
            ans = st.radio(f"Select choice for Q{i+1}", 
                          options=[row['A'], row['B'], row['C'], row['D']], 
                          key=f"q{i}", label_visibility="collapsed")
            user_answers.append(ans)
            st.write("---")

        submit = st.form_submit_button("Submit Assessment")

        if submit:
            if not name or not email:
                st.error("Please provide your name and email.")
            else:
                # 3. Score the test
                score = 0
                for i, row in test_pool.iterrows():
                    if user_answers[i] == row['Correct']:
                        score += 1
                
                percent = (score / len(test_pool)) * 100
                
                # 4. Save to 'Results' tab

                result_row
