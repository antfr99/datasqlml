import streamlit as st
import pandas as pd

# --- Load Movies CSV ---
movies_df = pd.read_csv("movies.csv")
movies_df.columns = movies_df.columns.str.strip()

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Introduction ---
st.title("SQL Movie Quiz 🎬")
st.write("""
This is a small personal project that combines **AI, Python, SQL, IMDb data, GitHub, and Streamlit**.  
The goal is to learn and practice SQL by interacting with questions based on my exported IMDb ratings list.  
Answer each question below and test your SQL knowledge while also exploring real movie data.
""")

# Initialize score counter
if "score" not in st.session_state:
    st.session_state.score = 0

def check_answer(question_key, answer, correct_answer, success_msg, df=None):
    if answer == correct_answer:
        st.success("✅ Correct! " + success_msg)
        st.session_state.score += 1
        if df is not None:
            st.dataframe(df, width="stretch", height=400)
    elif answer != "-- Select an option --":
        st.error("❌ Try again.")

# -------------------------
# EASY SQL QUESTIONS
# -------------------------
st.header("🟢 Easy SQL Questions")

# Q1
st.write("**Q1. Retrieve all movies from the dataset.**")
options1 = [
    "-- Select an option --",
    "SELECT * FROM movies",
    "SELECT Title, [IMDb Rating] FROM movies",
    "DELETE FROM movies"
]
ans1 = st.radio("", options1, key="q1")
check_answer("q1", ans1, "SELECT * FROM movies", "All movies are shown below:", movies_df)

# Q2
st.write("**Q2. Retrieve the Title and IMDb Rating for all movies.**")
options2 = [
    "-- Select an option --",
    "SELECT Title, [IMDb Rating] FROM movies",
    "SELECT COUNT(*) FROM movies",
    "SELECT * FROM movies WHERE [IMDb Rating] > 9"
]
ans2 = st.radio("", options2, key="q2")
check_answer("q2", ans2, "SELECT Title, [IMDb Rating] FROM movies", "Here are all titles and IMDb ratings:", movies_df[["Title", "IMDb Rating"]])

# Q3
st.write("**Q3. Find all movies where IMDb Rating is greater than or equal to 9.**")
options3 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE [IMDb Rating] >= 9",
    "SELECT * FROM movies WHERE Year >= 9",
    "SELECT Title FROM movies"
]
ans3 = st.radio("", options3, key="q3")
check_answer("q3", ans3, "SELECT * FROM movies WHERE [IMDb Rating] >= 9", "Movies rated 9 or higher by IMDb:", movies_df[movies_df["IMDb Rating"] >= 9].sort_values("IMDb Rating", ascending=False))

# Q4
st.write("**Q4. Count the total number of movies in the dataset.**")
options4 = [
    "-- Select an option --",
    "SELECT COUNT(*) FROM movies",
    "SELECT AVG([IMDb Rating]) FROM movies",
    "SELECT Title FROM movies"
]
ans4 = st.radio("", options4, key="q4")
if ans4 == "SELECT COUNT(*) FROM movies":
    st.success("✅ Correct! Total number of movies calculated.")
    st.session_state.score += 1
    st.metric("Total Movies", len(movies_df))
elif ans4 != "-- Select an option --":
    st.error("❌ Try again.")

# Q5
st.write("**Q5. Find all unique Title Types in the dataset.**")
options5 = [
    "-- Select an option --",
    "SELECT DISTINCT [Title Type] FROM movies",
    "SELECT * FROM movies",
    "SELECT Title FROM movies WHERE [Title Type] = 'movie'"
]
ans5 = st.radio("", options5, key="q5")
if ans5 == "SELECT DISTINCT [Title Type] FROM movies":
    st.success("✅ Correct! Unique Title Types are shown below:")
    st.session_state.score += 1
    st.write(movies_df["Title Type"].unique())
elif ans5 != "-- Select an option --":
    st.error("❌ Try again.")

# -------------------------
# INTERMEDIATE SQL QUESTIONS
# -------------------------
st.header("🟡 Intermediate SQL Questions")

# (Q6 – Q15 follow same pattern…)
# Example Q6:
st.write("**Q6. Find all movies released after the year 2015.**")
options6 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE Year > 2015",
    "SELECT * FROM movies WHERE [IMDb Rating] > 2015",
    "SELECT Year FROM movies"
]
ans6 = st.radio("", options6, key="q6")
check_answer("q6", ans6, "SELECT * FROM movies WHERE Year > 2015", "Movies released after 2015:", movies_df[movies_df["Year"] > 2015])

# (continue for Q7–Q15...)

# -------------------------
# DIFFICULT SQL QUESTIONS
# -------------------------
st.header("🔴 Difficult SQL Questions")

# (Q16 – Q25 go here, same structure as above, only using IMDb Rating)

# -------------------------
# FINAL SCORE
# -------------------------
st.write("---")
st.subheader("🎯 Quiz Completed")
st.write(f"You answered **{st.session_state.score}** questions correctly out of 25.")
