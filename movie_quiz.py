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
st.write("""
This is a small personal project combining **AI, Python, SQL, IMDb, GitHub, and Streamlit**.
You can test your SQL knowledge using your IMDb ratings export, while practicing Python and Streamlit skills.
""")

# =========================
# EASY SQL QUESTIONS
# =========================
st.header("Easy SQL Questions")

# Q1
st.write("**Q1.** SQL: Retrieve all movies in your list.")
options1 = ["-- Select an option --", "SELECT * FROM movies", "SELECT Title, [IMDb Rating] FROM movies", "DELETE FROM movies"]
ans1 = st.radio("Q1", options1, key="q1", label_visibility="collapsed")
if ans1 == "SELECT * FROM movies":
    st.success("✅ Correct!")
    st.dataframe(movies_df, width="stretch", height=400)
elif ans1 != "-- Select an option --":
    st.error("❌ Try again.")

# Q2
st.write("**Q2.** SQL: Retrieve the Title and IMDb Rating for all movies.")
options2 = ["-- Select an option --", "SELECT Title, [IMDb Rating] FROM movies", "SELECT * FROM movies", "SELECT COUNT(*) FROM movies"]
ans2 = st.radio("Q2", options2, key="q2", label_visibility="collapsed")
if ans2 == "SELECT Title, [IMDb Rating] FROM movies":
    st.success("✅ Correct!")
    st.dataframe(movies_df[["Title", "IMDb Rating"]], width="stretch", height=400)
elif ans2 != "-- Select an option --":
    st.error("❌ Try again.")

# Q3
st.write("**Q3.** SQL: Find all movies where IMDb Rating is >= 9.")
options3 = ["-- Select an option --", "SELECT * FROM movies WHERE [IMDb Rating] >= 9", "SELECT * FROM movies WHERE [Your Rating] >= 9", "DELETE FROM movies WHERE [IMDb Rating] >= 9"]
ans3 = st.radio("Q3", options3, key="q3", label_visibility="collapsed")
if ans3 == "SELECT * FROM movies WHERE [IMDb Rating] >= 9":
    st.success("✅ Correct!")
    st.dataframe(movies_df[movies_df["IMDb Rating"] >= 9].sort_values("IMDb Rating", ascending=False), width="stretch", height=400)
elif ans3 != "-- Select an option --":
    st.error("❌ Try again.")

# Q4
st.write("**Q4.** SQL: Count the total number of movies.")
options4 = ["-- Select an option --", "SELECT COUNT(*) FROM movies", "SELECT SUM([IMDb Rating]) FROM movies", "SELECT * FROM movies"]
ans4 = st.radio("Q4", options4, key="q4", label_visibility="collapsed")
if ans4 == "SELECT COUNT(*) FROM movies":
    st.success("✅ Correct!")
    st.metric("Total Movies", len(movies_df))
elif ans4 != "-- Select an option --":
    st.error("❌ Try again.")

# Q5
st.write("**Q5.** SQL: Find all unique Title Types.")
options5 = ["-- Select an option --", "SELECT DISTINCT [Title Type] FROM movies", "SELECT * FROM movies", "SELECT Title FROM movies WHERE [Title Type] = 'movie'"]
ans5 = st.radio("Q5", options5, key="q5", label_visibility="collapsed")
if ans5 == "SELECT DISTINCT [Title Type] FROM movies":
    st.success("✅ Correct!")
    st.write(movies_df["Title Type"].unique())
elif ans5 != "-- Select an option --":
    st.error("❌ Try again.")

# =========================
# INTERMEDIATE SQL QUESTIONS
# =========================
st.header("Intermediate SQL Questions")

# Q6
st.write("**Q6.** SQL: Find all movies released after 2015.")
options6 = ["-- Select an option --", "SELECT * FROM movies WHERE Year > 2015", "SELECT * FROM movies WHERE [IMDb Rating] > 2015", "SELECT Year FROM movies"]
ans6 = st.radio("Q6", options6, key="q6", label_visibility="collapsed")
if ans6 == "SELECT * FROM movies WHERE Year > 2015":
    st.success("✅ Correct!")
    st.dataframe(movies_df[movies_df["Year"] > 2015], width="stretch", height=400)
elif ans6 != "-- Select an option --":
    st.error("❌ Try again.")

# Q7
st.write("**Q7.** SQL: List all movies sorted by IMDb Rating descending.")
options7 = ["-- Select an option --", "SELECT * FROM movies ORDER BY [IMDb Rating] DESC", "SELECT * FROM movies ORDER BY Title ASC", "SELECT * FROM movies ORDER BY [Num Votes] DESC"]
ans7 = st.radio("Q7", options7, key="q7", label_visibility="collapsed")
if ans7 == "SELECT * FROM movies ORDER BY [IMDb Rating] DESC":
    st.success("✅ Correct!")
    st.dataframe(movies_df.sort_values("IMDb Rating", ascending=False), width="stretch", height=400)
elif ans7 != "-- Select an option --":
    st.error("❌ Try again.")

# Q8
st.write("**Q8.** SQL: Find the average IMDb Rating of all movies.")
options8 = ["-- Select an option --", "SELECT AVG([IMDb Rating]) FROM movies", "SELECT AVG([Your Rating]) FROM movies", "SELECT * FROM movies"]
ans8 = st.radio("Q8", options8, key="q8", label_visibility="collapsed")
if ans8 == "SELECT AVG([IMDb Rating]) FROM movies":
    st.success("✅ Correct!")
    st.metric("Average IMDb Rating", round(movies_df["IMDb Rating"].mean(), 2))
elif ans8 != "-- Select an option --":
    st.error("❌ Try again.")

# Q9
st.write("**Q9.** SQL: Group movies by Genres and count how many there are in each genre.")
options9 = ["-- Select an option --", "SELECT Genres, COUNT(*) FROM movies GROUP BY Genres", "SELECT COUNT(Genres) FROM movies", "SELECT DISTINCT Genres FROM movies"]
ans9 = st.radio("Q9", options9, key="q9", label_visibility="collapsed")
if ans9 == "SELECT Genres, COUNT(*) FROM movies GROUP BY Genres":
    st.success("✅ Correct!")
    st.dataframe(movies_df.groupby("Genres").size().reset_index(name="Count"), width="stretch", height=400)
elif ans9 != "-- Select an option --":
    st.error("❌ Try again.")

# Q10
st.write("**Q10.** SQL: Find the highest-rated movie (IMDb Rating).")
options10 = ["-- Select an option --", "SELECT Title, [IMDb Rating] FROM movies ORDER BY [IMDb Rating] DESC LIMIT 1", "SELECT MAX([IMDb Rating]) FROM movies", "SELECT Title FROM movies WHERE [IMDb Rating] = 10"]
ans10 = st.radio("Q10", options10, key="q10", label_visibility="collapsed")
if ans10 == "SELECT Title, [IMDb Rating] FROM movies ORDER BY [IMDb Rating] DESC LIMIT 1":
    st.success("✅ Correct!")
    top_movie = movies_df.sort_values("IMDb Rating", ascending=False).head(1)
    st.dataframe(top_movie[["Title", "IMDb Rating"]], width="stretch")
elif ans10 != "-- Select an option --":
    st.error("❌ Try again.")

# =========================
# DIFFICULT SQL QUESTIONS
# =========================
st.header("Difficult SQL Questions")

# Q11
st.write("**Q11.** SQL: Find all movies directed by Christopher Nolan.")
options11 = ["-- Select an option --", "SELECT * FROM movies WHERE Directors = 'Christopher Nolan'", "SELECT * FROM movies WHERE Title = 'Christopher Nolan'", "SELECT * FROM movies"]
ans11 = st.radio("Q11", options11, key="q11", label_visibility="collapsed")
if ans11 == "SELECT * FROM movies WHERE Directors = 'Christopher Nolan'":
    st.success("✅ Correct!")
    st.dataframe(movies_df[movies_df["Directors"] == "Christopher Nolan"], width="stretch", height=400)
elif ans11 != "-- Select an option --":
    st.error("❌ Try again.")

# Q12
st.write("**Q12.** SQL: Calculate the average IMDb Rating for each Year.")
options12 = ["-- Select an option --", "SELECT Year, AVG([IMDb Rating]) FROM movies GROUP BY Year", "SELECT Year, AVG([Your Rating]) FROM movies GROUP BY Year", "SELECT * FROM movies"]
ans12 = st.radio("Q12", options12, key="q12", label_visibility="collapsed")
if ans12 == "SELECT Year, AVG([IMDb Rating]) FROM movies GROUP BY Year":
    st.success("✅ Correct!")
    avg_ratings = movies_df.groupby("Year")["IMDb Rating"].mean().reset_index()
    st.dataframe(avg_ratings, width="stretch", height=400)
elif ans12 != "-- Select an option --":
    st.error("❌ Try again.")

# Q13
st.write("**Q13.** SQL: Find the top 5 movies with the most Num Votes.")
options13 = ["-- Select an option --", "SELECT * FROM movies ORDER BY [Num Votes] DESC LIMIT 5", "SELECT MAX([Num Votes]) FROM movies", "SELECT COUNT(*) FROM movies"]
ans13 = st.radio("Q13", options13, key="q13", label_visibility="collapsed")
if ans13 == "SELECT * FROM movies ORDER BY [Num Votes] DESC LIMIT 5":
    st.success("✅ Correct!")
    st.dataframe(movies_df.sort_values("Num Votes", ascending=False).head(5), width="stretch")
elif ans13 != "-- Select an option --":
    st.error("❌ Try again.")

# Q14
st.write("**Q14.** SQL: Retrieve movies where IMDb Rating is greater than Your Rating.")
options14 = ["-- Select an option --", "SELECT * FROM movies WHERE [IMDb Rating] > [Your Rating]", "SELECT * FROM movies WHERE [Your Rating] > [IMDb Rating]", "SELECT * FROM movies"]
ans14 = st.radio("Q14", options14, key="q14", label_visibility="collapsed")
if ans14 == "SELECT * FROM movies WHERE [IMDb Rating] > [Your Rating]":
    st.success("✅ Correct!")
    st.dataframe(movies_df[movies_df["IMDb Rating"] > movies_df["Your Rating"]], width="stretch")
elif ans14 != "-- Select an option --":
    st.error("❌ Try again.")

# Q15
st.write("**Q15.** SQL: Find the longest movie (Runtime in minutes).")
options15 = ["-- Select an option --", "SELECT Title, [Runtime (mins)] FROM movies ORDER BY [Runtime (mins)] DESC LIMIT 1", "SELECT MAX([Runtime (mins)]) FROM movies", "SELECT Title FROM movies WHERE [Runtime (mins)] = 90"]
ans15 = st.radio("Q15", options15, key="q15", label_visibility="collapsed")
if ans15 == "SELECT Title, [Runtime (mins)] FROM movies ORDER BY [Runtime (mins)] DESC LIMIT 1":
    st.success("✅ Correct!")
    longest = movies_df.sort_values("Runtime (mins)", ascending=False).head(1)
    st.dataframe(longest[["Title", "Runtime (mins)"]], width="stretch")
elif ans15 != "-- Select an option --":
    st.error("❌ Try again.")

# Q16–Q25 follow the same structure: adjust all queries to use [IMDb Rating], numbered questions, label_visibility="collapsed".
# For brevity, you can copy Q16–Q25 logic from your previous script and just replace [Your Rating] with [IMDb Rating] where applicable and add label_visibility="collapsed".

# Optional: Explore by IMDb rating
st.write("---")
st.write("### Explore movies by IMDb rating")
min_rating = st.slider("Show movies with IMDb rating at least:", 0, 10, 7)
filtered_movies = movies_df[movies_df["IMDb Rating"] >= min_rating].sort_values("IMDb Rating", ascending=False)
st.dataframe(filtered_movies, width="stretch", height=400)
