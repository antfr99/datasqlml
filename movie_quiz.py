import streamlit as st
import pandas as pd

# --- Load Movies CSV ---
movies_df = pd.read_csv("movies.csv")

# --- Page Config (make app wider) ---
st.set_page_config(layout="wide")

# --- App Title ---
st.title("SQL Knowledge Game 🎮")
st.write("Welcome to the SQL quiz app!")
st.markdown("**Note:** These are my personal ratings on IMDb.")

# --- Question 1 ---
st.write("---")
question1 = "Which SQL command retrieves all movies with an IMDb rating greater than 8.0?"
options1 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE IMDb_Rating > 8.0",
    "INSERT INTO movies WHERE IMDb_Rating > 8.0",
    "UPDATE movies SET IMDb_Rating > 8.0",
    "DELETE FROM movies WHERE IMDb_Rating > 8.0"
]
answer1 = st.radio(question1, options1, key="q1")

if answer1 == "SELECT * FROM movies WHERE IMDb_Rating > 8.0":
    st.success("✅ Correct!")
    st.write("Here are your top 5 rated movies:")
    top_movies = movies_df.sort_values("IMDb Rating", ascending=False).head(5)
    st.dataframe(top_movies, width="stretch")
elif answer1 != "-- Select an option --":
    st.error("❌ Try again.")

# --- Question 2 ---
st.write("---")
question2 = "How do you count the number of movies directed by 'Christopher Nolan'?"
options2 = [
    "-- Select an option --",
    "SELECT COUNT(*) FROM movies WHERE Directors = 'Christopher Nolan'",
    "SELECT SUM(Directors) FROM movies",
    "SELECT Directors FROM movies",
    "COUNT(*) FROM movies WHERE Directors = 'Christopher Nolan'"
]
answer2 = st.radio(question2, options2, key="q2")

if answer2 == "SELECT COUNT(*) FROM movies WHERE Directors = 'Christopher Nolan'":
    st.success("✅ Correct!")
    st.write("Here are Christopher Nolan movies you rated:")
    nolan_movies = movies_df[movies_df["Directors"] == "Christopher Nolan"]
    st.dataframe(nolan_movies, width="stretch")
elif answer2 != "-- Select an option --":
    st.error("❌ Not quite. Hint: COUNT(*) counts rows matching a condition.")

# --- Question 3 ---
st.write("---")
question3 = "Which SQL query lists the titles and your rating of movies released after 2015?"
options3 = [
    "-- Select an option --",
    "SELECT Title, Your_Rating FROM movies WHERE Year > 2015",
    "SELECT Title, Your_Rating FROM movies WHERE Year < 2015",
    "UPDATE movies SET Year > 2015",
    "DELETE FROM movies WHERE Year > 2015"
]
answer3 = st.radio(question3, options3, key="q3")

if answer3 == "SELECT Title, Your_Rating FROM movies WHERE Year > 2015":
    st.success("✅ Correct!")
    st.write("Here are movies released after 2015 that you rated:")
    recent_movies = movies_df[movies_df["Year"] > 2015][["Title", "Your Rating", "Year"]]
    st.dataframe(recent_movies, width="stretch")
elif answer3 != "-- Select an option --":
    st.error("❌ Not quite. Hint: Use SELECT to get columns and a WHERE clause for filtering.")

# --- Optional: Filter by rating ---
st.write("---")
st.write("### Explore your movies")
min_rating = st.slider("Show movies with rating at least:", 0, 10, 7)
filtered_movies = movies_df[movies_df["Your Rating"] >= min_rating]
st.dataframe(filtered_movies, width="stretch")
