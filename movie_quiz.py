import streamlit as st
import pandas as pd
import random

st.title("🎬 SQL & Movie Quiz Game")

st.write("""
This is a small personal project that uses **AI, Python, SQL, IMDb, GitHub, and Streamlit** together.  
It’s just for fun and to practice combining different applications and coding languages in one place.  
Enjoy the quiz! 🚀
""")

# --- Utility function to render each question ---
def render_question(qnum, key, text, correct, distractors, df_display=None):
    # Combine and shuffle options
    options = [correct] + distractors
    random.shuffle(options)
    options = ["-- Select an option --"] + options

    # Show question
    selection = st.radio(f"**{qnum}. {text}**", options, key=key)

    if selection == correct:
        st.success("✅ Correct!")

        # Display extra DataFrame if provided
        if df_display is not None:
            if callable(df_display):
                df_display = df_display()
            try:
                if isinstance(df_display, (pd.DataFrame, pd.Series)):
                    st.dataframe(df_display, width="stretch", height=320)
                else:
                    st.warning("⚠️ Extra details could not be displayed.")
            except Exception as e:
                st.warning(f"⚠️ Could not display details: {e}")

    elif selection != "-- Select an option --":
        st.error("❌ Try again.")

    return selection == correct


# --- Example Questions (replace with your real ones) ---
easy_questions = [
    {
        "key": "easy1",
        "text": "Which SQL command is used to retrieve data from a database?",
        "correct": "SELECT",
        "distractors": ["INSERT", "DELETE", "UPDATE"],
    },
    {
        "key": "easy2",
        "text": "What does IMDb stand for?",
        "correct": "Internet Movie Database",
        "distractors": ["International Movie Data Bureau", "Image Media Data Bank", "Independent Movie Directory"],
    },
]

intermediate_questions = [
    {
        "key": "int1",
        "text": "Which SQL clause is used to filter results?",
        "correct": "WHERE",
        "distractors": ["FROM", "ORDER BY", "GROUP BY"],
    },
    {
        "key": "int2",
        "text": "In IMDb, what type of score is shown as the main movie rating?",
        "correct": "IMDb Rating (out of 10)",
        "distractors": ["Critic Review Score", "Rotten Tomatoes %", "Viewer Likes"],
    },
]

difficult_questions = [
    {
        "key": "diff1",
        "text": "Which SQL keyword is used to remove duplicate rows from a query result?",
        "correct": "DISTINCT",
        "distractors": ["UNIQUE", "NODUP", "FILTER"],
    },
    {
        "key": "diff2",
        "text": "In SQL, which join returns only the rows that have matching values in both tables?",
        "correct": "INNER JOIN",
        "distractors": ["LEFT JOIN", "FULL OUTER JOIN", "CROSS JOIN"],
    },
]


# --- Main Quiz Execution ---
score = 0
total = 0
qnum = 1

# Easy
st.header("🟢 Easy SQL & Movie Questions")
for q in easy_questions:
    if render_question(qnum, q["key"], q["text"], q["correct"], q["distractors"]):
        score += 1
    total += 1
    qnum += 1

# Intermediate
st.header("🟡 Intermediate SQL & Movie Questions")
for q in intermediate_questions:
    if render_question(qnum, q["key"], q["text"], q["correct"], q["distractors"]):
        score += 1
    total += 1
    qnum += 1

# Difficult
st.header("🔴 Difficult SQL & Movie Questions")
for q in difficult_questions:
    if render_question(qnum, q["key"], q["text"], q["correct"], q["distractors"]):
        score += 1
    total += 1
    qnum += 1

# --- Final Score ---
st.subheader("📊 Your Final Score")
st.write(f"✅ You got **{score} / {total}** correct!")
