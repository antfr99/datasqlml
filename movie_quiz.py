import streamlit as st
import pandas as pd
import pandasql as ps

# --- Load CSVs ---
IMDB_Ratings = pd.read_csv("imdbratings.csv")
Personal_Ratings = pd.read_csv("myratings.csv")

# --- Ensure consistent column names ---
for df in [IMDB_Ratings, Personal_Ratings]:
    df.columns = df.columns.str.strip()

# --- Rename columns for clarity ---
Personal_Ratings = Personal_Ratings.rename(columns={"Your Rating": "Personal Ratings"})

# --- Ensure director & genre columns are cleaned ---
for df in [IMDB_Ratings, Personal_Ratings]:
    if "Director" in df.columns:
        df["Director"] = df["Director"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else None)
    if "Genre" in df.columns:
        df["Genre"] = df["Genre"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else None)

# --- Reset indices ---
IMDB_Ratings = IMDB_Ratings.reset_index(drop=True)
Personal_Ratings = Personal_Ratings.reset_index(drop=True)

# --- Streamlit Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb & Personal Ratings Project 🎬")
st.write("""
Explore your movies and IMDb ratings interactively, and try SQL queries across your datasets.
""")

# --- IMDb Ratings Table ---
st.write("---")
st.write("### IMDb Ratings")
min_rating = st.slider("Minimum IMDb rating to display:", 0, 10, 7, key="imdb_slider")
filtered_imdb = IMDB_Ratings[IMDB_Ratings["IMDb Rating"] >= min_rating].sort_values("IMDb Rating", ascending=False)
st.dataframe(filtered_imdb, width="stretch", height=400)

# --- Personal Ratings Table ---
st.write("---")
st.write("### Personal Ratings")
min_personal_rating = st.slider("Minimum Personal rating to display:", 0, 10, 7, key="personal_slider")
filtered_personal = Personal_Ratings[Personal_Ratings["Personal Ratings"] >= min_personal_rating].sort_values("Personal Ratings", ascending=False)
st.dataframe(filtered_personal, width="stretch", height=400)

# --- SQL Playground ---
st.write("---")
st.header("SQL Playground")
st.write("Run SQL queries on `IMDB_Ratings` or `Personal_Ratings`.")

default_query = """SELECT pr.Title,
       pr.[Personal Ratings],
       ir.[IMDb Rating],
       ABS(pr.[Personal Ratings] - ir.[IMDb Rating]) AS Rating_Diff
FROM Personal_Ratings pr
JOIN IMDB_Ratings ir
    ON pr.[Movie ID] = ir.[Movie ID]
WHERE ABS(pr.[Personal Ratings] - ir.[IMDb Rating]) > 2
ORDER BY Rating_Diff DESC
LIMIT 10;"""

user_query = st.text_area("Enter SQL query:", default_query, height=300, key="sql_area")

if st.button("Run SQL Query"):
    try:
        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"SQL Error: {e}")
