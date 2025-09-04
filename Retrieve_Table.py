import streamlit as st

st.title("SQL Commands Challenge 🎯")
st.write("Test your SQL knowledge with another quiz!")

# Question
question = "Which SQL command is used to remove a table from a database?"
options = ["DROP", "DELETE", "TRUNCATE", "REMOVE"]

# User selection
answer = st.radio(question, options)

# Feedback
if answer == "DROP":
    st.success("✅ Correct! DROP removes the table entirely.")
else:
    st.error("❌ Not quite. Hint: It completely deletes the table structure, not just the data.")
