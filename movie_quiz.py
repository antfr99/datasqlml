import streamlit as st
import pandas as pd
import pandasql as ps

# --- Robust CSV loader with guaranteed column normalization ---
def load_ratings_csv(file_path, personal=False):
    """
    Load CSV and normalize columns:
    - lowercase
    - underscores instead of spaces
    - renames 'Your Rating' to 'personal_ratings' if personal=True
    - renames 'Const' to 'movie_id'
    - cleans director and genre columns
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig', quotechar='"', skip_blank_lines=True, on_bad_lines='skip')

        # Strip spaces and normalize
        df.columns = [c.strip() for c in df.columns]

        # Standardize movie_id
        if "Const" in df.columns:
            df = df.rename(columns={"Const": "movie_id"})

        # Rename Your Rating if personal
        if personal and "Your Rating" in df.columns:
            df = df.rename(columns={"Your Rating": "personal_ratings"})

        # Clean director (first director only)
        if "Director" in df.columns:
            df["director"] = df["Director"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else None)
            df = df.drop(columns=["Director"])

        # Clean genre (first genre only)
        if "Genre" in df.columns:
            df["genre"] = df["Genre"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else None)
            df = df.drop(columns=["Genre"])

        # Ensure IMDb Rating column exists and normalize name
        if "IMDb Rating" in df.columns:
            df = df.rename(columns={"IMDb Rating": "imdb_rating"})

        df = df.reset_index(drop=True)
        return df

    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return pd.DataFrame()


# --- Load CSVs ---
IMDB_Ratings = load_ratings_csv("imdbratings.csv", personal=False)
Personal_Ratings = load_ratings_csv("myratings.csv", personal=True)

# --- Debug columns ---
st.write("IMDB_Ratings columns:", IMDB_Ratings.columns.tolist())
st.write("Personal_Ratings columns:", Personal_Ratings.columns.tolist())

# --- Streamlit Page ---
st.set_page_config(layout="wide")
st.title("IMDb & Personal Ratings Project 🎬")
st.write("Compare your personal ratings with IMDb ratings and explore the data.")


# --- IMDb Ratings Table ---
st.write("---")
st.write("### IMDb Ratings")
if not IMDB_Ratings.empty:
    min_rating = st.slider("Minimum IMDb rating:", 0, 10, 7, key="imdb_slider")
    IMDB_Ratings["imdb_rating"] = IMDB_Ratings["imdb_rating"].astype(float)
    filtered_imdb = IMDB_Ratings[IMDB_Ratings["imdb_rating"] >= min_rating].sort_values("imdb_rating", ascending=False)
    st.dataframe(filtered_imdb, width="stretch", height=400)
else:
    st.warning("IMDb Ratings CSV is empty or failed to load.")


# --- Personal Ratings Table ---
st.write("---")
st.write("### Personal Ratings")
if not Personal_Ratings.empty:
    min_personal_rating = st.slider("Minimum Personal rating:", 0, 10, 7, key="personal_slider")
    Personal_Ratings["personal_ratings"] = Personal_Ratings["personal_ratings"].astype(float)
    filtered_personal = Personal_Ratings[Personal_Ratings["personal_ratings"] >= min_personal_rating].sort_values("personal_ratings", ascending=False)
    st.dataframe(filtered_personal, width="stretch", height=400)
else:
    st.warning("Personal Ratings CSV is empty or failed to load.")


# --- SQL Playground ---
st.write("---")
st.header("SQL Playground")
st.write("Run SQL queries on `IMDB_Ratings` or `Personal_Ratings` using normalized column names.")

default_query = """SELECT pr.title,
       pr.personal_ratings,
       ir.imdb_rating,
       ABS(pr.personal_ratings - ir.imdb_rating) AS rating_diff
FROM Personal_Ratings pr
JOIN IMDB_Ratings ir
    ON pr.movie_id = ir.movie_id
WHERE ABS(pr.personal_ratings - ir.imdb_rating) > 2
ORDER BY rating_diff DESC
LIMIT 10;"""

user_query = st.text_area("Enter SQL query:", default_query, height=300, key="sql_area")

if st.button("Run SQL Query"):
    try:
        # Ensure numeric types
        if "personal_ratings" in Personal_Ratings.columns:
            Personal_Ratings["personal_ratings"] = Personal_Ratings["personal_ratings"].astype(float)
        if "imdb_rating" in IMDB_Ratings.columns:
            IMDB_Ratings["imdb_rating"] = IMDB_Ratings["imdb_rating"].astype(float)

        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"SQL Error: {e}")
