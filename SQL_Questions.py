import streamlit as st

st.title("SQL Knowledge Game 🎮")
st.write("Welcome to the SQL quiz app!")

# --- Question 1 ---
question1 = "Which SQL command retrieves data from a table?"
options1 = ["INSERT", "SELECT", "UPDATE", "DELETE"]
answer1 = st.radio(question1, options1, key="q1")

if answer1 == "SELECT":
    st.success("✅ Correct!")
elif answer1:
    st.error("❌ Try again.")

# --- Question 2 ---
question2 = "Which SQL command is used to remove a table from a database?"
options2 = ["DROP", "DELETE", "TRUNCATE", "REMOVE"]
answer2 = st.radio(question2, options2, key="q2")

if answer2 == "DROP":
    st.success("✅ Correct! DROP removes the table entirely.")
elif answer2:
    st.error("❌ Not quite. Hint: It completely deletes the table structure, not just the data.")
