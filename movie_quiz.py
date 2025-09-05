import streamlit as st
import pandas as pd
import pandasql as ps

# --- Load Movies CSV ---
movies_df = pd.read_csv("movies.csv")
movies_df.columns = movies_df.columns.str.strip()

# --- Clean IMDB_Ratings for quiz and IMDb filter ---
IMDB_Ratings = movies_df.copy()

# 2️⃣ Rename 'Const' to 'Movie ID'
if "Const" in IMDB_Ratings.columns:
    IMDB_Ratings = IMDB_Ratings.rename(columns={"Const": "Movie ID"})

# 3️⃣ Remove unnecessary columns
cols_to_drop = ["Your Rating", "Date Rated", "Original Title", "URL"]
IMDB_Ratings = IMDB_Ratings.drop(columns=[c for c in cols_to_drop if c in IMDB_Ratings.columns])

# 4️⃣ Keep only the first director per movie and rename to 'director'
if "Directors" in IMDB_Ratings.columns:
    IMDB_Ratings["director"] = IMDB_Ratings["Directors"].fillna("").apply(
        lambda x: x.split(",")[0].strip() if x else ""
    )
    IMDB_Ratings = IMDB_Ratings.drop(columns=["Directors"])

IMDB_Ratings = IMDB_Ratings.reset_index(drop=True)

# --- Create Personal Ratings table ---
Personal_Ratings = movies_df.copy()

# Keep only the first director and rename column
if "Directors" in Personal_Ratings.columns:
    Personal_Ratings["Director"] = Personal_Ratings["Directors"].fillna("").apply(
        lambda x: x.split(",")[0].strip() if x else ""
    )

# Rename columns
rename_map = {
    "Const": "Movie ID",
    "Your Rating": "Personal Ratings"
}
Personal_Ratings = Personal_Ratings.rename(columns=rename_map)

# Keep only desired columns
desired_cols = [
    "Movie ID", "Personal Ratings", "Date Rated", "Title", "URL",
    "Title Type", "Runtime (mins)", "Year",
    "Release Date", "Director", "Genre"  # keep Genre for SQL
]
Personal_Ratings = Personal_Ratings[[c for c in desired_cols if c in Personal_Ratings.columns]]
Personal_Ratings = Personal_Ratings.reset_index(drop=True)

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Project Description ---
st.title("Movie SQL Sandbox & SQL Quiz 🎬")
st.write(
    """
This is a small personal project combining **Python, SQL, IMDb, GitHub, and Streamlit** which provides a SQL Sandbox and also tests your SQL knowledge.
"""
)

# --- Single SQL Playground for both tables ---
st.write("---")
st.header("Try SQL Queries on IMDB Ratings and my Personal Film Ratings")
st.write(
    """
Type any SQL query against either `IMDB_Ratings` or `Personal_Ratings`.

Example 1: `SELECT Title, [IMDb Rating] FROM IMDB_Ratings WHERE [IMDb Rating] > 8`  
Example 2: `SELECT Title, [Personal Ratings] FROM Personal_Ratings WHERE [Personal Ratings] >= 7`
"""
)


user_query = st.text_area(
    "Enter SQL query for either table:",
    "SELECT * FROM IMDB_Ratings LIMIT 5",
    key="sql_playground"
)

if st.button("Run SQL Query"):
    try:
        # Both tables are available in locals()
        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error in SQL query: {e}")

# --- Explore movies by IMDb rating ---        

st.write("---")
st.write("### Explore movies by IMDb Ratings")
min_rating = st.slider(
    "Show movies with IMDb rating at least:",
    0, 10, 7,
    key="imdb_slider"
)
filtered_movies = IMDB_Ratings[IMDB_Ratings["IMDb Rating"] >= min_rating].sort_values("IMDb Rating", ascending=False)

# Drop Genre only for display
st.dataframe(
    filtered_movies.drop(columns=["Genres"], errors="ignore"),
    width="stretch",
    height=400
)

# --- Personal Ratings Table ---
# --- Personal Ratings Table ---
st.write("---")
st.write("### Personal Ratings")

# 🎛️ Add a slider filter for Personal Ratings
min_personal_rating = st.slider(
    "Show movies with Personal rating at least:",
    0, 10, 7,
    key="personal_slider"
)

filtered_personal = Personal_Ratings[
    Personal_Ratings["Personal Ratings"] >= min_personal_rating
].sort_values("Personal Ratings", ascending=False)

st.dataframe(
    filtered_personal.drop(columns=["Genre"], errors="ignore"),
    width="stretch",
    height=400
)

# =====================
# SQL QUIZ
# =====================
# ---------------- Q1 ----------------
st.write("**Q1.** List the top 10 movies where Personal rating differs from IMDb rating by more than 2 points, ordered by difference descending.")

options1 = [
    "-- Select an option --",
    """SELECT Title, [Personal Ratings], [IMDb Rating]
FROM Personal_Ratings
WHERE [Personal Ratings] - [IMDb Rating] > 2
ORDER BY [Personal Ratings] DESC
LIMIT 10;""",  # Incorrect
    """SELECT mr.Title, mr.[Personal Ratings], mc.[IMDb Rating],
       ABS(mr.[Personal Ratings] - mc.[IMDb Rating]) AS Rating_Diff
FROM Personal_Ratings mr
JOIN IMDB_Ratings mc ON mr.[Movie ID] = mc.[Movie ID]
WHERE mr.[Personal Ratings] IS NOT NULL
  AND ABS(mr.[Personal Ratings] - mc.[IMDb Rating]) > 2
ORDER BY Rating_Diff DESC
LIMIT 10;""",  # ✅ correct
    """SELECT mr.Title, mr.[Personal Ratings], mc.[IMDb Rating],
       ABS(mr.[Personal Ratings] - mc.[IMDb Rating]) AS Rating_Diff
FROM Personal_Ratings mr
JOIN IMDB_Ratings mc ON mr.[Movie ID] = mc.[Movie ID]
WHERE mr.[Personal Ratings] IS NOT NULL
ORDER BY Rating_Diff ASC
LIMIT 10;"""  # Incorrect
]

ans1 = st.radio("Q1", options1, key="q1", label_visibility="collapsed")

if ans1 == options1[2]:
    st.success("✅ Correct!")
    result_q1 = ps.sqldf(options1[2], locals())
    st.dataframe(result_q1, width="stretch", height=400)
    st.write("**Explanation:**")
    st.write("1️⃣ Incorrect because it does not join with IMDB_Ratings to get IMDb rating.")
    st.write("3️⃣ Incorrect because it orders ascending instead of descending.")
elif ans1 != "-- Select an option --":
    st.error("❌ Try again.")


# ---------------- Q2 ----------------
st.write("---")
st.write("**Q2.** Find the highest-rated movie for each year (IMDb rating) and order by year ascending.")

options2 = [
    "-- Select an option --",
    """SELECT Year, Title, MAX([IMDb Rating]) FROM IMDB_Ratings GROUP BY Year;""",  # Incorrect
    """SELECT Year, Title, [IMDb Rating]
FROM IMDB_Ratings
ORDER BY Year ASC;""",  # Incorrect
    """SELECT Year, Title, [IMDb Rating]
FROM IMDB_Ratings mc1
WHERE [IMDb Rating] = (
    SELECT MAX([IMDb Rating])
    FROM IMDB_Ratings mc2
    WHERE mc2.Year = mc1.Year
)
ORDER BY Year ASC;"""  # ✅ correct
]

ans2 = st.radio("Q2", options2, key="q2", label_visibility="collapsed")

if ans2 == options2[3]:
    st.success("✅ Correct!")
    result_q2 = ps.sqldf(options2[3], locals())
    st.dataframe(result_q2, width="stretch", height=400)
    st.write("**Explanation:**")
    st.write("1️⃣ Incorrect because SQLite syntax doesn’t match expected result per year.")
    st.write("2️⃣ Incorrect because it does not select max per year.")
elif ans2 != "-- Select an option --":
    st.error("❌ Try again.")


# ---------------- Q3 ----------------
st.write("---")
st.write("**Q3.** Show your top 10 rated movies by difference from IMDb, descending.")

options3 = [
    "-- Select an option --",
    """SELECT mr.Title, mr.[Personal Ratings], mc.[IMDb Rating], 
       (mr.[Personal Ratings] - mc.[IMDb Rating]) AS Diff
FROM Personal_Ratings mr
JOIN IMDB_Ratings mc ON mr.[Movie ID] = mc.[Movie ID]
WHERE mr.[Personal Ratings] IS NOT NULL
ORDER BY Diff DESC
LIMIT 10;""",  # ✅ correct
    """SELECT Title, [Personal Ratings], [IMDb Rating] 
FROM Personal_Ratings
ORDER BY Diff DESC
LIMIT 10;""",  # Incorrect (Diff not defined)
    """SELECT mr.Title, mr.[Personal Ratings], mc.[IMDb Rating], 
       (mr.[Personal Ratings] - mc.[IMDb Rating]) AS Diff
FROM Personal_Ratings mr
JOIN IMDB_Ratings mc ON mr.[Movie ID] = mc.[Movie ID]
WHERE mr.[Personal Ratings] IS NOT NULL
ORDER BY Diff ASC
LIMIT 10;"""  # Incorrect (wrong sort)
]

ans3 = st.radio("Q3", options3, key="q3", label_visibility="collapsed")

if ans3 == options3[1]:
    st.success("✅ Correct!")
    result_q3 = ps.sqldf(options3[1], locals())
    st.dataframe(result_q3, width="stretch", height=400)
    st.write("**Explanation:**")
    st.write("2️⃣ Incorrect because Diff is not defined.")
    st.write("3️⃣ Incorrect because ASC orders smallest difference first.")
elif ans3 != "-- Select an option --":
    st.error("❌ Try again.")


# ---------------- Q4 ----------------
st.write("---")
st.write("**Q4.** Find top 10 movie pairs by the same director with largest IMDb rating difference.")

options4 = [
    "-- Select an option --",
    """SELECT director, Title FROM IMDB_Ratings;""",  # Incorrect
    """SELECT m1.director, m1.Title AS Movie1, m2.Title AS Movie2,
ABS(m1.[IMDb Rating] - m2.[IMDb Rating]) AS Rating_Diff
FROM IMDB_Ratings m1
JOIN IMDB_Ratings m2 ON m1.director = m2.director
AND m1.[Movie ID] < m2.[Movie ID]
ORDER BY Rating_Diff DESC
LIMIT 10;""",  # ✅ correct
    """SELECT m1.director, m1.Title AS Movie1, m2.Title AS Movie2,
ABS(m1.[IMDb Rating] - m2.[IMDb Rating]) AS Rating_Diff
FROM IMDB_Ratings m1
JOIN IMDB_Ratings m2 ON m1.director = m2.director
ORDER BY Rating_Diff ASC
LIMIT 10;"""  # Incorrect
]

ans4 = st.radio("Q4", options4, key="q4", label_visibility="collapsed")

if ans4 == options4[2]:
    st.success("✅ Correct!")
    result_q4 = ps.sqldf(options4[2], locals())
    st.dataframe(result_q4, width="stretch", height=400)
    st.write("**Explanation:**")
    st.write("1️⃣ Incorrect because query does nothing useful.")
    st.write("3️⃣ Incorrect because ASC and missing ID filter create duplicates.")
elif ans4 != "-- Select an option --":
    st.error("❌ Try again.")


# ---------------- Q5 ----------------
st.write("---")
st.write("**Q5.** Find movies released in the same year with identical runtime (self-join).")

options6 = [
    "-- Select an option --",
    """SELECT Title, Year, [Runtime (mins)] FROM IMDB_Ratings;""",  # Incorrect
    """SELECT m1.Title AS Movie1, m2.Title AS Movie2, m1.Year, m1.[Runtime (mins)]
FROM IMDB_Ratings m1
JOIN IMDB_Ratings m2 
ON m1.Year = m2.Year AND m1.[Runtime (mins)] = m2.[Runtime (mins)]
AND m1.[Movie ID] < m2.[Movie ID]
ORDER BY m1.Year DESC, m1.[Runtime (mins)] DESC
LIMIT 10;""",  # ✅ correct
    """SELECT m1.Title AS Movie1, m2.Title AS Movie2, m1.Year, m1.[Runtime (mins)]
FROM IMDB_Ratings m1
JOIN IMDB_Ratings m2 
ON m1.Year = m2.Year
ORDER BY m1.Year DESC
LIMIT 10;"""  # Incorrect
]

ans6 = st.radio("Q6", options6, key="q6", label_visibility="collapsed")

if ans6 == options6[2]:
    st.success("✅ Correct!")
    result_q6 = ps.sqldf(options6[2], locals())
    st.dataframe(result_q6, width="stretch", height=400)
    st.write("**Explanation:**")
    st.write("1️⃣ Incorrect because query does not pair movies correctly (no self-join logic).")
    st.write("3️⃣ Incorrect because it only matches on year, not runtime, and also allows duplicates.")
elif ans6 != "-- Select an option --":
    st.error("❌ Try again.")
