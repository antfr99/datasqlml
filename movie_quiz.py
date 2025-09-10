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

# 4️⃣ Keep only the first director per movie and rename to 'director'
if "Directors" in IMDB_Ratings.columns:
    IMDB_Ratings["director"] = IMDB_Ratings["Directors"].fillna("").apply(
        lambda x: x.split(",")[0].strip() if x else ""
    )
    IMDB_Ratings = IMDB_Ratings.drop(columns=["Directors"])

# ✅ Clean director column (remove blanks, placeholders, normalize)
bad_tokens = {"", "nan", "none", "null", "n/a", "unknown"}
IMDB_Ratings["director"] = (
    IMDB_Ratings["director"]
    .astype(str)
    .str.strip()
    .replace(bad_tokens, None)   # replace bad tokens with real None/NaN
)

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
st.title("IMDb/SQL Data Project 🎬")
st.write(
    """
This is a small imdb data project combining Python Packages ( Streamlit, Pandas , PandasQL ), ChatGPT, SQL, GitHub, and Streamlit.
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




# --- Explore movies by IMDb rating ---        

st.write("---")
st.write("### IMDb Ratings")
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

user_query = st.text_area(
    "Enter SQL query for either table:",
    """SELECT pr.Title,
              pr.[Personal Ratings],
              ir.[IMDb Rating],
              ABS(pr.[Personal Ratings] - ir.[IMDb Rating]) AS Rating_Diff
       FROM Personal_Ratings pr
       JOIN IMDB_Ratings ir 
           ON pr.[Movie ID] = ir.[Movie ID]
       WHERE ABS(pr.[Personal Ratings] - ir.[IMDb Rating]) > 2
       ORDER BY Rating_Diff DESC
       LIMIT 10;""",
    key="sql_playground",
    height=500  # ⬅️ default is ~150, so 300 doubles it
)

if st.button("Run SQL Query"):
    try:
        # Both tables are available in locals()
        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error in SQL query: {e}")