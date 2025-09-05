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

# =========================
# DIFFICULT SQL QUESTIONS CONTINUED
# =========================

# Q16
st.write("**Q16.** SQL: Find the movie with the second-highest IMDb Rating using DENSE_RANK().")
options16 = [
    "-- Select an option --",
    "SELECT Title, [IMDb Rating] FROM (SELECT Title, [IMDb Rating], DENSE_RANK() OVER (ORDER BY [IMDb Rating] DESC) AS rnk FROM movies) t WHERE rnk = 2",
    "SELECT Title, MAX([IMDb Rating]) FROM movies",
    "SELECT * FROM movies WHERE [IMDb Rating] = 2"
]
ans16 = st.radio("Q16", options16, key="q16", label_visibility="collapsed")
if ans16.startswith("SELECT Title, [IMDb Rating] FROM (SELECT"):
    st.success("✅ Correct!")
    movies_df["Rank"] = movies_df["IMDb Rating"].rank(method="dense", ascending=False)
    second_highest = movies_df[movies_df["Rank"] == 2][["Title", "IMDb Rating"]]
    st.dataframe(second_highest, width="stretch")
elif ans16 != "-- Select an option --":
    st.error("❌ Try again.")

# Q17
st.write("**Q17.** SQL: Use a CTE to find the top-rated movie (IMDb Rating) per director.")
options17 = [
    "-- Select an option --",
    "WITH cte AS (SELECT Directors, Title, [IMDb Rating], ROW_NUMBER() OVER (PARTITION BY Directors ORDER BY [IMDb Rating] DESC) AS rn FROM movies) SELECT * FROM cte WHERE rn = 1",
    "SELECT Directors, MAX([IMDb Rating]) FROM movies GROUP BY Directors",
    "SELECT DISTINCT Directors FROM movies"
]
ans17 = st.radio("Q17", options17, key="q17", label_visibility="collapsed")
if ans17.startswith("WITH cte AS"):
    st.success("✅ Correct!")
    top_per_director = movies_df.sort_values(["Directors", "IMDb Rating"], ascending=[True, False]).groupby("Directors").head(1)
    st.dataframe(top_per_director[["Directors", "Title", "IMDb Rating"]], width="stretch")
elif ans17 != "-- Select an option --":
    st.error("❌ Try again.")

# Q18
st.write("**Q18.** SQL: Calculate a running total of Num Votes ordered by Release Date.")
options18 = [
    "-- Select an option --",
    "SELECT [Release Date], [Num Votes], SUM([Num Votes]) OVER (ORDER BY [Release Date]) AS RunningTotal FROM movies",
    "SELECT SUM([Num Votes]) FROM movies",
    "SELECT * FROM movies ORDER BY [Num Votes]"
]
ans18 = st.radio("Q18", options18, key="q18", label_visibility="collapsed")
if ans18.startswith("SELECT [Release Date], [Num Votes], SUM([Num Votes])"):
    st.success("✅ Correct!")
    running = movies_df.sort_values("Release Date").copy()
    running["Running Total"] = running["Num Votes"].cumsum()
    st.dataframe(running[["Release Date", "Num Votes", "Running Total"]], width="stretch")
elif ans18 != "-- Select an option --":
    st.error("❌ Try again.")

# Q19
st.write("**Q19.** SQL: Find directors who have movies in the most unique Genres.")
options19 = [
    "-- Select an option --",
    "SELECT Directors, COUNT(DISTINCT Genres) AS GenreCount FROM movies GROUP BY Directors ORDER BY GenreCount DESC",
    "SELECT Directors, COUNT(*) FROM movies GROUP BY Directors",
    "SELECT DISTINCT Genres FROM movies"
]
ans19 = st.radio("Q19", options19, key="q19", label_visibility="collapsed")
if ans19.startswith("SELECT Directors, COUNT(DISTINCT Genres)"):
    st.success("✅ Correct!")
    genre_diversity = movies_df.groupby("Directors")["Genres"].nunique().reset_index(name="Unique Genres")
    st.dataframe(genre_diversity.sort_values("Unique Genres", ascending=False), width="stretch")
elif ans19 != "-- Select an option --":
    st.error("❌ Try again.")

# Q20
st.write("**Q20.** SQL: Compare IMDb Rating of each movie with the one released just before it (LAG function).")
options20 = [
    "-- Select an option --",
    "SELECT Title, [IMDb Rating], LAG([IMDb Rating]) OVER (ORDER BY [Release Date]) AS PrevRating FROM movies",
    "SELECT Title, [IMDb Rating] FROM movies ORDER BY [Release Date]",
    "SELECT * FROM movies WHERE [IMDb Rating] > 5"
]
ans20 = st.radio("Q20", options20, key="q20", label_visibility="collapsed")
if ans20.startswith("SELECT Title, [IMDb Rating], LAG"):
    st.success("✅ Correct!")
    lagged = movies_df.sort_values("Release Date").copy()
    lagged["Prev Rating"] = lagged["IMDb Rating"].shift(1)
    st.dataframe(lagged[["Release Date", "Title", "IMDb Rating", "Prev Rating"]], width="stretch")
elif ans20 != "-- Select an option --":
    st.error("❌ Try again.")

# Q21
st.write("**Q21.** SQL: Perform a self-join to find movies with the same director released on the same year.")
options21 = [
    "-- Select an option --",
    "SELECT a.Title, b.Title, a.Directors, a.Year FROM movies a JOIN movies b ON a.Directors = b.Directors AND a.Year = b.Year AND a.Title <> b.Title",
    "SELECT * FROM movies WHERE Directors IS NOT NULL",
    "SELECT DISTINCT Directors FROM movies"
]
ans21 = st.radio("Q21", options21, key="q21", label_visibility="collapsed")
if ans21.startswith("SELECT a.Title, b.Title"):
    st.success("✅ Correct!")
    self_join = movies_df.merge(movies_df, on=["Directors", "Year"], suffixes=("_a", "_b"))
    self_join = self_join[self_join["Title_a"] != self_join["Title_b"]]
    st.dataframe(self_join[["Title_a", "Title_b", "Directors", "Year"]], width="stretch")
elif ans21 != "-- Select an option --":
    st.error("❌ Try again.")

# Q22
st.write("**Q22.** SQL: Find years between earliest and latest Release Date where no movie was released.")
options22 = [
    "-- Select an option --",
    "SELECT y.Year FROM (SELECT MIN([Release Date]) AS MinYear, MAX([Release Date]) AS MaxYear FROM movies) r CROSS JOIN Years y WHERE y.Year BETWEEN r.MinYear AND r.MaxYear AND y.Year NOT IN (SELECT DISTINCT Year FROM movies)",
    "SELECT DISTINCT Year FROM movies",
    "SELECT * FROM movies ORDER BY [Release Date]"
]
ans22 = st.radio("Q22", options22, key="q22", label_visibility="collapsed")
if ans22.startswith("SELECT y.Year FROM (SELECT MIN([Release Date])"):
    st.success("✅ Correct!")
    release_years = pd.to_datetime(movies_df["Release Date"], errors="coerce").dt.year.dropna().astype(int)
    all_years = pd.Series(range(release_years.min(), release_years.max() + 1))
    missing_years = all_years[~all_years.isin(release_years.unique())]
    st.write("Years with no movies:", missing_years.tolist())
elif ans22 != "-- Select an option --":
    st.error("❌ Try again.")

# Q23
st.write("**Q23.** SQL: Find genres where average IMDb Rating is below the overall average.")
options23 = [
    "-- Select an option --",
    "SELECT Genres FROM movies GROUP BY Genres HAVING AVG([IMDb Rating]) < (SELECT AVG([IMDb Rating]) FROM movies)",
    "SELECT AVG([IMDb Rating]) FROM movies",
    "SELECT DISTINCT Genres FROM movies"
]
ans23 = st.radio("Q23", options23, key="q23", label_visibility="collapsed")
if ans23.startswith("SELECT Genres FROM movies GROUP BY Genres HAVING"):
    st.success("✅ Correct!")
    overall_avg = movies_df["IMDb Rating"].mean()
    low_genres = movies_df.groupby("Genres")["IMDb Rating"].mean().reset_index().query("`IMDb Rating` < @overall_avg")
    st.dataframe(low_genres, width="stretch")
elif ans23 != "-- Select an option --":
    st.error("❌ Try again.")

# Q24
st.write("**Q24.** SQL: Find the IMDb Rating value that appears most frequently.")
options24 = [
    "-- Select an option --",
    "SELECT [IMDb Rating], COUNT(*) AS cnt FROM movies GROUP BY [IMDb Rating] ORDER BY cnt DESC LIMIT 1",
    "SELECT MAX([IMDb Rating]) FROM movies",
    "SELECT DISTINCT [IMDb Rating] FROM movies"
]
ans24 = st.radio("Q24", options24, key="q24", label_visibility="collapsed")
if ans24.startswith("SELECT [IMDb Rating], COUNT(*)"):
    st.success("✅ Correct!")
    most_common = movies_df["IMDb Rating"].mode()[0]
    freq = (movies_df["IMDb Rating"] == most_common).sum()
    st.metric("Most Common IMDb Rating", most_common, help=f"Appears {freq} times")
elif ans24 != "-- Select an option --":
    st.error("❌ Try again.")

# Q25
st.write("**Q25.** SQL: Find average IMDb Rating per Year and difference to Your Rating.")
options25 = [
    "-- Select an option --",
    "SELECT Year, AVG([IMDb Rating]) AS AvgIMDb, AVG([Your Rating]) AS AvgYour, (AVG([Your Rating]) - AVG([IMDb Rating])) AS Diff FROM movies GROUP BY Year ORDER BY Year",
    "SELECT AVG([IMDb Rating]), AVG([Your Rating]) FROM movies",
    "SELECT Year, [IMDb Rating], [Your Rating] FROM movies"
]
ans25 = st.radio("Q25", options25, key="q25", label_visibility="collapsed")
if ans25.startswith("SELECT Year, AVG([IMDb Rating]) AS AvgIMDb"):
    st.success("✅ Correct!")
    year_compare = movies_df.groupby("Year")[["IMDb Rating", "Your Rating"]].mean().reset_index()
    year_compare["Diff"] = year_compare["Your Rating"] - year_compare["IMDb Rating"]
    st.dataframe(year_compare.sort_values("Year"), width="stretch")
elif ans25 != "-- Select an option --":
    st.error("❌ Try again.")


# Optional: Explore by IMDb rating
st.write("---")
st.write("### Explore movies by IMDb rating")
min_rating = st.slider("Show movies with IMDb rating at least:", 0, 10, 7)
filtered_movies = movies_df[movies_df["IMDb Rating"] >= min_rating].sort_values("IMDb Rating", ascending=False)
st.dataframe(filtered_movies, width="stretch", height=400)
