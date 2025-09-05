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
    st.dataframe(movies_df, use_container_width=True, height=400)
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
    st.dataframe(movies_df[["Title", "Your Rating"]], use_container_width=True, height=400)
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
        use_container_width=True, height=400
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
q6 = "SQL: Find the average IMDb Rating for each Genres type."
options6 = [
    "-- Select an option --",
    "SELECT Genres, AVG([IMDb Rating]) FROM movies GROUP BY Genres",
    "SELECT AVG([IMDb Rating]) FROM movies",
    "SELECT DISTINCT Genres FROM movies"
]
ans6 = st.radio(q6, options6, key="q6")

if ans6 == "SELECT Genres, AVG([IMDb Rating]) FROM movies GROUP BY Genres":
    st.success("✅ Correct!")
    avg_genres = movies_df.groupby("Genres", dropna=False)["IMDb Rating"].mean().reset_index()
    st.dataframe(avg_genres.sort_values("IMDb Rating", ascending=False), use_container_width=True, height=400)
elif ans6 != "-- Select an option --":
    st.error("❌ Try again.")

# Q7
st.write("---")
q7 = "SQL: Find genres that have an average Your Rating of 7 or higher."
options7 = [
    "-- Select an option --",
    "SELECT Genres, AVG([Your Rating]) FROM movies GROUP BY Genres HAVING AVG([Your Rating]) >= 7",
    "SELECT Genres, AVG([Your Rating]) FROM movies",
    "SELECT * FROM movies WHERE [Your Rating] >= 7"
]
ans7 = st.radio(q7, options7, key="q7")

if ans7 == "SELECT Genres, AVG([Your Rating]) FROM movies GROUP BY Genres HAVING AVG([Your Rating]) >= 7":
    st.success("✅ Correct!")
    having_genres = (
        movies_df.groupby("Genres")["Your Rating"].mean().reset_index()
        .query("`Your Rating` >= 7")
    )
    st.dataframe(having_genres.sort_values("Your Rating", ascending=False), use_container_width=True, height=400)
elif ans7 != "-- Select an option --":
    st.error("❌ Try again.")

# Q8
st.write("---")
q8 = "SQL: Find movies where Your Rating is greater than the average Your Rating of all entries."
options8 = [
    "-- Select an option --",
    "SELECT Title FROM movies WHERE [Your Rating] > (SELECT AVG([Your Rating]) FROM movies)",
    "SELECT Title FROM movies WHERE [Your Rating] >= 9",
    "SELECT * FROM movies ORDER BY [Your Rating]"
]
ans8 = st.radio(q8, options8, key="q8")

if ans8 == "SELECT Title FROM movies WHERE [Your Rating] > (SELECT AVG([Your Rating]) FROM movies)":
    st.success("✅ Correct!")
    avg_rating = movies_df["Your Rating"].mean()
    above_avg = movies_df[movies_df["Your Rating"] > avg_rating][["Title", "Your Rating"]]
    st.dataframe(above_avg.sort_values("Your Rating", ascending=False), use_container_width=True, height=400)
elif ans8 != "-- Select an option --":
    st.error("❌ Try again.")

# Q9
st.write("---")
q9 = "SQL: Find all movies directed by Quentin Tarantino."
options9 = [
    "-- Select an option --",
    "SELECT * FROM movies WHERE Directors = 'Quentin Tarantino'",
    "SELECT * FROM movies WHERE Title = 'Quentin Tarantino'",
    "SELECT DISTINCT Directors FROM movies"
]
ans9 = st.radio(q9, options9, key="q9")

if ans9 == "SELECT * FROM movies WHERE Directors = 'Quentin Tarantino'":
    st.success("✅ Correct!")
    tarantino = movies_df[movies_df["Directors"].str.contains("Quentin Tarantino", na=False)]
    st.dataframe(tarantino, use_container_width=True, height=400)
elif ans9 != "-- Select an option --":
    st.error("❌ Try again.")

# Q10
st.write("---")
q10 = "SQL: Categorize Your Ratings into 'Great' (>= 9), 'Good' (7-8), and 'Okay' (<= 6)."
options10 = [
    "-- Select an option --",
    "SELECT Title, [Your Rating], CASE WHEN [Your Rating] >= 9 THEN 'Great' WHEN [Your Rating] BETWEEN 7 AND 8 THEN 'Good' ELSE 'Okay' END AS Category FROM movies",
    "SELECT Title, [Your Rating] FROM movies",
    "SELECT * FROM movies WHERE [Your Rating] >= 7"
]
ans10 = st.radio(q10, options10, key="q10")

if ans10.startswith("SELECT Title, [Your Rating], CASE"):
    st.success("✅ Correct!")
    categorized = movies_df[["Title", "Your Rating"]].copy()
    categorized["Category"] = pd.cut(
        categorized["Your Rating"],
        bins=[-float("inf"), 6, 8, float("inf")],
        labels=["Okay", "Good", "Great"]
    )
    st.dataframe(categorized, use_container_width=True, height=400)
elif ans10 != "-- Select an option --":
    st.error("❌ Try again.")

# Q11
st.write("---")
q11 = "SQL: Find the earliest and latest-rated movies by Date Rated."
options11 = [
    "-- Select an option --",
    "SELECT * FROM movies ORDER BY [Date Rated] ASC LIMIT 1; SELECT * FROM movies ORDER BY [Date Rated] DESC LIMIT 1",
    "SELECT MIN([Date Rated]), MAX([Date Rated]) FROM movies",
    "SELECT * FROM movies WHERE [Your Rating] = 10"
]
ans11 = st.radio(q11, options11, key="q11")

if ans11.startswith("SELECT * FROM movies ORDER BY [Date Rated] ASC"):
    st.success("✅ Correct!")
    earliest = movies_df.sort_values("Date Rated").head(1)
    latest = movies_df.sort_values("Date Rated").tail(1)
    st.write("**Earliest Rated Movie:**")
    st.dataframe(earliest, use_container_width=True)
    st.write("**Latest Rated Movie:**")
    st.dataframe(latest, use_container_width=True)
elif ans11 != "-- Select an option --":
    st.error("❌ Try again.")

# Q12
st.write("---")
q12 = "SQL: Find the top 5 directors based on the average Your Rating of their movies."
options12 = [
    "-- Select an option --",
    "SELECT Directors, AVG([Your Rating]) AS AvgRating FROM movies GROUP BY Directors ORDER BY AvgRating DESC LIMIT 5",
    "SELECT Directors, COUNT(*) FROM movies GROUP BY Directors",
    "SELECT DISTINCT Directors FROM movies"
]
ans12 = st.radio(q12, options12, key="q12")

if ans12.startswith("SELECT Directors, AVG([Your Rating])"):
    st.success("✅ Correct!")
    top_directors = (
        movies_df.groupby("Directors")["Your Rating"].mean().reset_index()
        .sort_values("Your Rating", ascending=False).head(5)
    )
    st.dataframe(top_directors, use_container_width=True)
elif ans12 != "-- Select an option --":
    st.error("❌ Try again.")

# Q13
st.write("---")
q13 = "SQL: List the top 10 movies with the longest runtime."
options13 = [
    "-- Select an option --",
    "SELECT * FROM movies ORDER BY [Runtime (mins)] DESC LIMIT 10",
    "SELECT * FROM movies ORDER BY [Your Rating] DESC LIMIT 10",
    "SELECT * FROM movies WHERE [Runtime (mins)] > 120"
]
ans13 = st.radio(q13, options13, key="q13")

if ans13.startswith("SELECT * FROM movies ORDER BY [Runtime (mins)] DESC LIMIT 10"):
    st.success("✅ Correct!")
    long_movies = movies_df.sort_values("Runtime (mins)", ascending=False).head(10)
    st.dataframe(long_movies, use_container_width=True)
elif ans13 != "-- Select an option --":
    st.error("❌ Try again.")

# Q14
st.write("---")
q14 = "SQL: List all distinct Genres."
options14 = [
    "-- Select an option --",
    "SELECT DISTINCT Genres FROM movies",
    "SELECT * FROM movies",
    "SELECT Genres, COUNT(*) FROM movies"
]
ans14 = st.radio(q14, options14, key="q14")

if ans14 == "SELECT DISTINCT Genres FROM movies":
    st.success("✅ Correct!")
    st.write(movies_df["Genres"].unique())
elif ans14 != "-- Select an option --":
    st.error("❌ Try again.")

# Q15
st.write("---")
q15 = "SQL: Count how many movies you rated each Year."
options15 = [
    "-- Select an option --",
    "SELECT Year, COUNT(*) FROM movies GROUP BY Year ORDER BY Year",
    "SELECT COUNT(*) FROM movies",
    "SELECT DISTINCT Year FROM movies"
]
ans15 = st.radio(q15, options15, key="q15")

if ans15.startswith("SELECT Year, COUNT(*) FROM movies GROUP BY Year"):
    st.success("✅ Correct!")
    year_counts = movies_df.groupby("Year").size().reset_index(name="Count")
    st.dataframe(year_counts.sort_values("Year"), use_container_width=True)
elif ans15 != "-- Select an option --":
    st.error("❌ Try again.")


# -------------------------
# DIFFICULT SQL QUESTIONS
# -------------------------

# Q16
st.write("---")
q16 = "SQL: Find the movie with the second-highest Your Rating using DENSE_RANK()."
options16 = [
    "-- Select an option --",
    "SELECT Title, [Your Rating] FROM (SELECT Title, [Your Rating], DENSE_RANK() OVER (ORDER BY [Your Rating] DESC) AS rnk FROM movies) t WHERE rnk = 2",
    "SELECT Title, MAX([Your Rating]) FROM movies",
    "SELECT * FROM movies WHERE [Your Rating] = 2"
]
ans16 = st.radio(q16, options16, key="q16")

if ans16.startswith("SELECT Title, [Your Rating] FROM (SELECT"):
    st.success("✅ Correct!")
    movies_df["Rank"] = movies_df["Your Rating"].rank(method="dense", ascending=False)
    second_highest = movies_df[movies_df["Rank"] == 2][["Title", "Your Rating"]]
    st.dataframe(second_highest, use_container_width=True)
elif ans16 != "-- Select an option --":
    st.error("❌ Try again.")

# Q17
st.write("---")
q17 = "SQL: Use a CTE to find the top-rated movie (Your Rating) per director."
options17 = [
    "-- Select an option --",
    "WITH cte AS (SELECT Directors, Title, [Your Rating], ROW_NUMBER() OVER (PARTITION BY Directors ORDER BY [Your Rating] DESC) AS rn FROM movies) SELECT * FROM cte WHERE rn = 1",
    "SELECT Directors, MAX([Your Rating]) FROM movies GROUP BY Directors",
    "SELECT DISTINCT Directors FROM movies"
]
ans17 = st.radio(q17, options17, key="q17")

if ans17.startswith("WITH cte AS"):
    st.success("✅ Correct!")
    top_per_director = (
        movies_df.sort_values(["Directors", "Your Rating"], ascending=[True, False])
        .groupby("Directors").head(1)
    )
    st.dataframe(top_per_director[["Directors", "Title", "Your Rating"]], use_container_width=True)
elif ans17 != "-- Select an option --":
    st.error("❌ Try again.")

# Q18
st.write("---")
q18 = "SQL: Calculate a running total of Num Votes ordered by Release Date."
options18 = [
    "-- Select an option --",
    "SELECT [Release Date], [Num Votes], SUM([Num Votes]) OVER (ORDER BY [Release Date]) AS RunningTotal FROM movies",
    "SELECT SUM([Num Votes]) FROM movies",
    "SELECT * FROM movies ORDER BY [Num Votes]"
]
ans18 = st.radio(q18, options18, key="q18")

if ans18.startswith("SELECT [Release Date], [Num Votes], SUM([Num Votes])"):
    st.success("✅ Correct!")
    running = movies_df.sort_values("Release Date").copy()
    running["Running Total"] = running["Num Votes"].cumsum()
    st.dataframe(running[["Release Date", "Num Votes", "Running Total"]], use_container_width=True)
elif ans18 != "-- Select an option --":
    st.error("❌ Try again.")

# Q19
st.write("---")
q19 = "SQL: Find directors who have movies in the most unique Genres."
options19 = [
    "-- Select an option --",
    "SELECT Directors, COUNT(DISTINCT Genres) AS GenreCount FROM movies GROUP BY Directors ORDER BY GenreCount DESC",
    "SELECT Directors, COUNT(*) FROM movies GROUP BY Directors",
    "SELECT DISTINCT Genres FROM movies"
]
ans19 = st.radio(q19, options19, key="q19")

if ans19.startswith("SELECT Directors, COUNT(DISTINCT Genres)"):
    st.success("✅ Correct!")
    genre_diversity = (
        movies_df.groupby("Directors")["Genres"].nunique().reset_index(name="Unique Genres")
    )
    st.dataframe(genre_diversity.sort_values("Unique Genres", ascending=False), use_container_width=True)
elif ans19 != "-- Select an option --":
    st.error("❌ Try again.")

# Q20
st.write("---")
q20 = "SQL: Compare Your Rating of each movie with the one you rated just before it (LAG function)."
options20 = [
    "-- Select an option --",
    "SELECT Title, [Your Rating], LAG([Your Rating]) OVER (ORDER BY [Date Rated]) AS PrevRating FROM movies",
    "SELECT Title, [Your Rating] FROM movies ORDER BY [Date Rated]",
    "SELECT * FROM movies WHERE [Your Rating] > 5"
]
ans20 = st.radio(q20, options20, key="q20")

if ans20.startswith("SELECT Title, [Your Rating], LAG"):
    st.success("✅ Correct!")
    lagged = movies_df.sort_values("Date Rated").copy()
    lagged["Prev Rating"] = lagged["Your Rating"].shift(1)
    st.dataframe(lagged[["Date Rated", "Title", "Your Rating", "Prev Rating"]], use_container_width=True)
elif ans20 != "-- Select an option --":
    st.error("❌ Try again.")

# Q21
st.write("---")
q21 = "SQL: Perform a self-join to find movies with the same director rated on the same Date Rated."
options21 = [
    "-- Select an option --",
    "SELECT a.Title, b.Title, a.Directors, a.[Date Rated] FROM movies a JOIN movies b ON a.Directors = b.Directors AND a.[Date Rated] = b.[Date Rated] AND a.Const <> b.Const",
    "SELECT * FROM movies WHERE Directors IS NOT NULL",
    "SELECT DISTINCT Directors FROM movies"
]
ans21 = st.radio(q21, options21, key="q21")

if ans21.startswith("SELECT a.Title, b.Title"):
    st.success("✅ Correct!")
    self_join = movies_df.merge(
        movies_df,
        on=["Directors", "Date Rated"],
        suffixes=("_a", "_b")
    )
    self_join = self_join[self_join["Const_a"] != self_join["Const_b"]]
    st.dataframe(self_join[["Title_a", "Title_b", "Directors", "Date Rated"]], use_container_width=True)
elif ans21 != "-- Select an option --":
    st.error("❌ Try again.")

# Q22
st.write("---")
q22 = "SQL: Find years between the earliest and latest Release Date where you didn’t rate any movie."
options22 = [
    "-- Select an option --",
    "SELECT y.Year FROM (SELECT MIN([Release Date]) AS MinYear, MAX([Release Date]) AS MaxYear FROM movies) r CROSS JOIN Years y WHERE y.Year BETWEEN r.MinYear AND r.MaxYear AND y.Year NOT IN (SELECT DISTINCT Year FROM movies)",
    "SELECT DISTINCT Year FROM movies",
    "SELECT * FROM movies ORDER BY [Release Date]"
]
ans22 = st.radio(q22, options22, key="q22")

if ans22.startswith("SELECT y.Year FROM (SELECT MIN([Release Date])"):
    st.success("✅ Correct!")
    release_years = pd.to_datetime(movies_df["Release Date"], errors="coerce").dt.year.dropna().astype(int)
    all_years = pd.Series(range(release_years.min(), release_years.max() + 1))
    missing_years = all_years[~all_years.isin(release_years.unique())]
    st.write("Years with no ratings:", missing_years.tolist())
elif ans22 != "-- Select an option --":
    st.error("❌ Try again.")

# Q23
st.write("---")
q23 = "SQL: Find genres where the average Your Rating is below the overall average of all Your Ratings."
options23 = [
    "-- Select an option --",
    "SELECT Genres FROM movies GROUP BY Genres HAVING AVG([Your Rating]) < (SELECT AVG([Your Rating]) FROM movies)",
    "SELECT AVG([Your Rating]) FROM movies",
    "SELECT DISTINCT Genres FROM movies"
]
ans23 = st.radio(q23, options23, key="q23")

if ans23.startswith("SELECT Genres FROM movies GROUP BY Genres HAVING"):
    st.success("✅ Correct!")
    overall_avg = movies_df["Your Rating"].mean()
    low_genres = (
        movies_df.groupby("Genres")["Your Rating"].mean().reset_index()
        .query("`Your Rating` < @overall_avg")
    )
    st.dataframe(low_genres, use_container_width=True)
elif ans23 != "-- Select an option --":
    st.error("❌ Try again.")

# Q24
st.write("---")
q24 = "SQL: Find the Your Rating value that appears most frequently."
options24 = [
    "-- Select an option --",
    "SELECT [Your Rating], COUNT(*) AS cnt FROM movies GROUP BY [Your Rating] ORDER BY cnt DESC LIMIT 1",
    "SELECT MAX([Your Rating]) FROM movies",
    "SELECT DISTINCT [Your Rating] FROM movies"
]
ans24 = st.radio(q24, options24, key="q24")

if ans24.startswith("SELECT [Your Rating], COUNT(*)"):
    st.success("✅ Correct!")
    most_common = movies_df["Your Rating"].mode()[0]
    freq = (movies_df["Your Rating"] == most_common).sum()
    st.metric("Most Common Rating", most_common, help=f"Appears {freq} times")
elif ans24 != "-- Select an option --":
    st.error("❌ Try again.")

# Q25
st.write("---")
q25 = "SQL: Find the average Your Rating and IMDb Rating per Year, and the difference between them."
options25 = [
    "-- Select an option --",
    "SELECT Year, AVG([Your Rating]) AS AvgYour, AVG([IMDb Rating]) AS AvgIMDb, (AVG([Your Rating]) - AVG([IMDb Rating])) AS Diff FROM movies GROUP BY Year ORDER BY Year",
    "SELECT AVG([Your Rating]), AVG([IMDb Rating]) FROM movies",
    "SELECT Year, [Your Rating], [IMDb Rating] FROM movies"
]
ans25 = st.radio(q25, options25, key="q25")

if ans25.startswith("SELECT Year, AVG([Your Rating])"):
    st.success("✅ Correct!")
    year_compare = (
        movies_df.groupby("Year")[["Your Rating", "IMDb Rating"]].mean().reset_index()
    )
    year_compare["Diff"] = year_compare["Your Rating"] - year_compare["IMDb Rating"]
    st.dataframe(year_compare.sort_values("Year"), use_container_width=True)
elif ans25 != "-- Select an option --":
    st.error("❌ Try again.")

# --- Optional: Filter by IMDb rating ---
st.write("---")
st.write("### Explore movies by IMDb rating")
min_rating = st.slider("Show movies with IMDb rating at least:", 0, 10, 7)
filtered_movies = movies_df[movies_df["IMDb Rating"] >= min_rating].sort_values("IMDb Rating", ascending=False)
st.dataframe(filtered_movies, width="stretch", height=400)