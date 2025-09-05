import streamlit as st
import pandas as pd

# --- Load Movies CSV ---
movies_df = pd.read_csv("movies.csv")

# --- Clean column names ---
movies_df.columns = movies_df.columns.str.strip()

# --- Page Config ---
st.set_page_config(layout="wide")

# --- App Title ---
st.title("SQL Movie Quiz 🎬")
st.write("Test your SQL knowledge using my IMDb ratings export!")

# -------------------------
# EASY SQL QUESTIONS
# -------------------------

# Q1
st.write("---")
q1 = "SQL: Retrieve all movies you've rated."
options1 = [
    "-- Select an option --",
    "SELECT * FROM movies",
    "SELECT Title, Your Rating FROM movies",
    "DELETE FROM movies"
]
ans1 = st.radio(q1, options1, key="q1")

if ans1 == "SELECT * FROM movies":
    st.success("✅ Correct!")
    st.dataframe(movies_df, width="stretch", height=400)
elif ans1 != "-- Select an option --":
    st.error("❌ Try again.")

# Q2
st.write("---")
q2 = "SQL: Retrieve the Title and Your Rating for all movies in your list."
options2 = [
    "-- Select an option --",
    "SELECT Title, [Your Rating] FROM movies",
    "SELECT * FROM movies",
    "SELECT COUNT(*) FROM movies"
]
ans2 = st.radio(q2, options2, key="q2")

if ans2 == "SELECT Title, [Your Rating] FROM movies":
    st.success("✅ Correct!")
    st.dataframe(movies_df[["Title", "Your Rating"]], width="stretch", height=400)
elif ans2 != "-- Select an option --":
    st.error("❌ Try again.")

# Q3
st.write("---")
q3 = "SQL: Find all movies where Your Rating is greater than or equal to 9."
options3 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE [Your Rating] >= 9",
    "SELECT * FROM movies WHERE [IMDb Rating] >= 9",
    "DELETE FROM movies WHERE [Your Rating] >= 9"
]
ans3 = st.radio(q3, options3, key="q3")

if ans3 == "SELECT * FROM movies WHERE [Your Rating] >= 9":
    st.success("✅ Correct!")
    st.dataframe(
        movies_df[movies_df["Your Rating"] >= 9].sort_values("Your Rating", ascending=False),
        width="stretch", height=400
    )
elif ans3 != "-- Select an option --":
    st.error("❌ Try again.")

# Q4
st.write("---")
q4 = "SQL: Count the total number of movies you've rated."
options4 = [
    "-- Select an option --",
    "SELECT COUNT(*) FROM movies",
    "SELECT SUM([Your Rating]) FROM movies",
    "SELECT * FROM movies"
]
ans4 = st.radio(q4, options4, key="q4")

if ans4 == "SELECT COUNT(*) FROM movies":
    st.success("✅ Correct!")
    st.metric("Total Movies Rated", len(movies_df))
elif ans4 != "-- Select an option --":
    st.error("❌ Try again.")

# Q5
st.write("---")
q5 = "SQL: Find all unique Title Types in your ratings list."
options5 = [
    "-- Select an option --",
    "SELECT DISTINCT [Title Type] FROM movies",
    "SELECT * FROM movies",
    "SELECT Title FROM movies WHERE [Title Type] = 'movie'"
]
ans5 = st.radio(q5, options5, key="q5")

if ans5 == "SELECT DISTINCT [Title Type] FROM movies":
    st.success("✅ Correct!")
    st.write(movies_df["Title Type"].unique())
elif ans5 != "-- Select an option --":
    st.error("❌ Try again.")

# -------------------------
# INTERMEDIATE SQL QUESTIONS
# -------------------------

# Q6
st.write("---")
q6 = "SQL: Find all movies released after the year 2015."
options6 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE Year > 2015",
    "SELECT * FROM movies WHERE [Your Rating] > 2015",
    "SELECT Year FROM movies"
]
ans6 = st.radio(q6, options6, key="q6")

if ans6 == "SELECT * FROM movies WHERE Year > 2015":
    st.success("✅ Correct!")
    st.dataframe(movies_df[movies_df["Year"] > 2015], width="stretch", height=400)
elif ans6 != "-- Select an option --":
    st.error("❌ Try again.")

# Q7
st.write("---")
q7 = "SQL: List all movies sorted by Your Rating in descending order."
options7 = [
    "-- Select an option --",
    "SELECT * FROM movies ORDER BY [Your Rating] DESC",
    "SELECT * FROM movies ORDER BY [IMDb Rating] DESC",
    "SELECT * FROM movies ORDER BY Title ASC"
]
ans7 = st.radio(q7, options7, key="q7")

if ans7 == "SELECT * FROM movies ORDER BY [Your Rating] DESC":
    st.success("✅ Correct!")
    st.dataframe(movies_df.sort_values("Your Rating", ascending=False), width="stretch", height=400)
elif ans7 != "-- Select an option --":
    st.error("❌ Try again.")

# Q8
st.write("---")
q8 = "SQL: Find the average IMDb Rating of all movies."
options8 = [
    "-- Select an option --",
    "SELECT AVG([IMDb Rating]) FROM movies",
    "SELECT AVG([Your Rating]) FROM movies",
    "SELECT * FROM movies"
]
ans8 = st.radio(q8, options8, key="q8")

if ans8 == "SELECT AVG([IMDb Rating]) FROM movies":
    st.success("✅ Correct!")
    st.metric("Average IMDb Rating", round(movies_df["IMDb Rating"].mean(), 2))
elif ans8 != "-- Select an option --":
    st.error("❌ Try again.")

# Q9
st.write("---")
q9 = "SQL: Group movies by Genre and count how many there are in each genre."
options9 = [
    "-- Select an option --",
    "SELECT Genres, COUNT(*) FROM movies GROUP BY Genres",
    "SELECT COUNT(Genres) FROM movies",
    "SELECT DISTINCT Genres FROM movies"
]
ans9 = st.radio(q9, options9, key="q9")

if ans9 == "SELECT Genres, COUNT(*) FROM movies GROUP BY Genres":
    st.success("✅ Correct!")
    st.dataframe(movies_df.groupby("Genres").size().reset_index(name="Count"), width="stretch", height=400)
elif ans9 != "-- Select an option --":
    st.error("❌ Try again.")

# Q10
st.write("---")
q10 = "SQL: Find the highest-rated movie (Your Rating)."
options10 = [
    "-- Select an option --",
    "SELECT Title, [Your Rating] FROM movies ORDER BY [Your Rating] DESC LIMIT 1",
    "SELECT MAX([Your Rating]) FROM movies",
    "SELECT Title FROM movies WHERE [Your Rating] = 10"
]
ans10 = st.radio(q10, options10, key="q10")

if ans10 == "SELECT Title, [Your Rating] FROM movies ORDER BY [Your Rating] DESC LIMIT 1":
    st.success("✅ Correct!")
    top_movie = movies_df.sort_values("Your Rating", ascending=False).head(1)
    st.dataframe(top_movie[["Title", "Your Rating"]], width="stretch")
elif ans10 != "-- Select an option --":
    st.error("❌ Try again.")

# Q11
st.write("---")
q11 = "SQL: Find all movies directed by Christopher Nolan."
options11 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE Directors = 'Christopher Nolan'",
    "SELECT * FROM movies WHERE Title = 'Christopher Nolan'",
    "SELECT * FROM movies"
]
ans11 = st.radio(q11, options11, key="q11")

if ans11 == "SELECT * FROM movies WHERE Directors = 'Christopher Nolan'":
    st.success("✅ Correct!")
    st.dataframe(movies_df[movies_df["Directors"] == "Christopher Nolan"], width="stretch", height=400)
elif ans11 != "-- Select an option --":
    st.error("❌ Try again.")

# Q12
st.write("---")
q12 = "SQL: Calculate the average Your Rating for each Year."
options12 = [
    "-- Select an option --",
    "SELECT Year, AVG([Your Rating]) FROM movies GROUP BY Year",
    "SELECT Year, AVG([IMDb Rating]) FROM movies GROUP BY Year",
    "SELECT * FROM movies"
]
ans12 = st.radio(q12, options12, key="q12")

if ans12 == "SELECT Year, AVG([Your Rating]) FROM movies GROUP BY Year":
    st.success("✅ Correct!")
    avg_ratings = movies_df.groupby("Year")["Your Rating"].mean().reset_index()
    st.dataframe(avg_ratings, width="stretch", height=400)
elif ans12 != "-- Select an option --":
    st.error("❌ Try again.")

# Q13
st.write("---")
q13 = "SQL: Find the top 5 movies with the most Num Votes."
options13 = [
    "-- Select an option --",
    "SELECT * FROM movies ORDER BY [Num Votes] DESC LIMIT 5",
    "SELECT MAX([Num Votes]) FROM movies",
    "SELECT COUNT(*) FROM movies"
]
ans13 = st.radio(q13, options13, key="q13")

if ans13 == "SELECT * FROM movies ORDER BY [Num Votes] DESC LIMIT 5":
    st.success("✅ Correct!")
    st.dataframe(movies_df.sort_values("Num Votes", ascending=False).head(5), width="stretch")
elif ans13 != "-- Select an option --":
    st.error("❌ Try again.")

# Q14
st.write("---")
q14 = "SQL: Retrieve movies where Your Rating is greater than the IMDb Rating."
options14 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE [Your Rating] > [IMDb Rating]",
    "SELECT * FROM movies WHERE [IMDb Rating] > [Your Rating]",
    "SELECT * FROM movies"
]
ans14 = st.radio(q14, options14, key="q14")

if ans14 == "SELECT * FROM movies WHERE [Your Rating] > [IMDb Rating]":
    st.success("✅ Correct!")
    st.dataframe(movies_df[movies_df["Your Rating"] > movies_df["IMDb Rating"]], width="stretch")
elif ans14 != "-- Select an option --":
    st.error("❌ Try again.")

# Q15
st.write("---")
q15 = "SQL: Find the longest movie (Runtime in minutes)."
options15 = [
    "-- Select an option --",
    "SELECT Title, [Runtime (mins)] FROM movies ORDER BY [Runtime (mins)] DESC LIMIT 1",
    "SELECT MAX([Runtime (mins)]) FROM movies",
    "SELECT Title FROM movies WHERE [Runtime (mins)] = 90"
]
ans15 = st.radio(q15, options15, key="q15")

if ans15 == "SELECT Title, [Runtime (mins)] FROM movies ORDER BY [Runtime (mins)] DESC LIMIT 1":
    st.success("✅ Correct!")
    longest = movies_df.sort_values("Runtime (mins)", ascending=False).head(1)
    st.dataframe(longest[["Title", "Runtime (mins)"]], width="stretch")
elif ans15 != "-- Select an option --":
    st.error("❌ Try again.")

# -------------------------
# DIFFICULT SQL QUESTIONS
# -------------------------
# (Paste the Difficult Q16–Q25 block I gave you earlier here – already updated with width="stretch")
