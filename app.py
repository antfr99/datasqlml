import streamlit as st

st.title("SQL Knowledge Game 🎮")

st.write("Welcome to the SQL quiz app!")

question = "Which SQL command retrieves data from a table?"
options = ["INSERT", "SELECT", "UPDATE", "DELETE"]

answer = st.radio("Choose one:", options)

if answer == "SELECT":
    st.success("✅ Correct!")
else:
    st.error("❌ Try again.")
