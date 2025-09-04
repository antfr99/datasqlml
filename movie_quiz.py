import streamlit as st
import pandas as pd

# --- Load Movies CSV ---
movies_df = pd.read_csv("movies.csv")

# --- Clean column names ---
movies_df.columns = movies_df.columns.str.strip()

# --- Page Config ---
st.set_page_config(layout="wide")

# --- App Title ---
st.title("SQL & Python Movie Quiz 🎮")
st.write("Welcome to the SQL & Python quiz app!")
st.markdown(
    "**Note:** Learn about SQL and Python using my IMDb movie ratings. "
    "The database contains only films I have rated - 1339 titles since 2012."
)

# --- QUESTION 1: SQL ---
st.write("---")
question1 = "SQL: Which command retrieves all movies with an IMDb rating greater than 8.0?"
options1 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE [IMDb Rating] > 8.0",
    "INSERT INTO movies WHERE [IMDb Rating] > 8.0",
    "UPDATE movies SET [IMDb Rating] > 8.0",
    "DELETE FROM movies WHERE [IMDb Rating] > 8.0"
]
answer1 = st.radio(question1, options1, key="q1")

if answer1 == "SELECT * FROM movies WHERE [IMDb Rating] > 8.0":
    st.success("✅ Correct!")
    st.write("Here are all movies with IMDb rating above 8.0:")
    top_movies = movies_df[movies_df["IMDb Rating"] > 8.0].sort_values("IMDb Rating", ascending=False)
    st.dataframe(top_movies, width="stretch", height=400)
elif answer1 != "-- Select an option --":
    st.error("❌ Try again.")

# --- QUESTION 2: Python ---
st.write("---")
question2 = "Python: How do you filter movies with IMDb rating above 9.0 using pandas?"
options2 = [
    "-- Select an option --",
    "movies_df[movies_df['IMDb Rating'] > 9.0]",
    "movies_df['IMDb Rating'] > 9.0",
    "movies_df.filter('IMDb Rating' > 9.0)",
    "movies_df.where('IMDb Rating' > 9.0)"
]
answer2 = st.radio(question2, options2, key="q2")

if answer2 == "movies_df[movies_df['IMDb Rating'] > 9.0]":
    st.success("✅ Correct!")
    st.write("Here are movies with IMDb rating above 9.0:")
    top_rated = movies_df[movies_df["IMDb Rating"] > 9.0].sort_values("IMDb Rating", ascending=False)
    st.dataframe(top_rated, width="stretch", height=400)
elif answer2 != "-- Select an option --":
    st.error("❌ Not quite. Hint: Use pandas boolean indexing.")

# --- QUESTION 3: SQL ---
st.write("---")
question3 = "SQL: Which query lists the titles and IMDb rating of movies released after 2015?"
options3 = [
    "-- Select an option --",
    "SELECT Title, [IMDb Rating] FROM movies WHERE Year > 2015",
    "SELECT Title, [IMDb Rating] FROM movies WHERE Year < 2015",
    "UPDATE movies SET Year > 2015",
    "DELETE FROM movies WHERE Year > 2015"
]
answer3 = st.radio(question3, options3, key="q3")

if answer3 == "SELECT Title, [IMDb Rating] FROM movies WHERE Year > 2015":
    st.success("✅ Correct!")
    st.write("Here are movies released after 2015:")
    recent_movies = movies_df[movies_df["Year"] > 2015][["Title", "IMDb Rating", "Year"]].sort_values("IMDb Rating", ascending=False)
    st.dataframe(recent_movies, width="stretch", height=400)
elif answer3 != "-- Select an option --":
    st.error("❌ Not quite. Hint: Use SELECT with WHERE clause.")

# --- QUESTION 4: Python ---
st.write("---")
question4 = "Python: How do you select the 'Title' and 'IMDb Rating' columns for movies after 2015?"
options4 = [
    "-- Select an option --",
    "movies_df[movies_df['Year'] > 2015][['Title','IMDb Rating']]",
    "movies_df[['Title','IMDb Rating'] > 2015]",
    "movies_df.filter(['Title','IMDb Rating'], Year>2015)",
    "movies_df[['Title','IMDb Rating']].where(Year>2015)"
]
answer4 = st.radio(question4, options4, key="q4")

if answer4 == "movies_df[movies_df['Year'] > 2015][['Title','IMDb Rating']]":
    st.success("✅ Correct!")
    st.write("Here are movies released after 2015:")
    recent_movies_py = movies_df[movies_df["Year"] > 2015][["Title", "IMDb Rating", "Year"]].sort_values("IMDb Rating", ascending=False)
    st.dataframe(recent_movies_py, width="stretch", height=400)
elif answer4 != "-- Select an option --":
    st.error("❌ Not quite. Hint: Use pandas boolean indexing and column selection.")

# --- Optional: Filter by IMDb rating ---
st.write("---")
st.write("### Explore movies by IMDb rating")
min_rating = st.slider("Show movies with IMDb rating at least:", 0, 10, 7)
filtered_movies = movies_df[movies_df["IMDb Rating"] >= min_rating].sort_values("IMDb Rating", ascending=False)
st.dataframe(filtered_movies, width="stretch", height=400)
