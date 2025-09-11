import streamlit as st
import pandas as pd
import pandasql as ps

# --- Robust CSV loader ---
def load_ratings_csv(file_path, personal=False):
    """
    Load ratings CSV files, normalize column names, and clean director/genre columns.
    Args:
        file_path (str): CSV file path
        personal (bool): If True, renames 'Your Rating' to 'personal_ratings'
    Returns:
        pd.DataFrame: cleaned DataFrame
    """
    try:
        df = pd.read_csv(
            file_path,
            encoding='utf-8-sig',
            quotechar='"',
            skip_blank_lines=True,
            on_bad_lines='skip'
        )

        # Strip spaces and normalize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Rename 'your_rating' to 'personal_ratings'
        if personal and "your_rating" in df.columns:
            df = df.rename(columns={"your_rating": "personal_ratings"})

        # Standardize movie_id
        if "const" in df.columns:
            df = df.rename(columns={"const": "movie_id"})

        # Clean director column (first director only)
        if "director" in df.columns:
            df["director"] = df["director"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else None)

        # Clean genre column (first genre only)
        if "genre" in df.columns:
            df["genre"] = df["genre"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else None)

        df = df.reset_index(drop=True)
        return df

    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return pd.DataFrame()


# --- Load CSVs ---
IMDB_Ratings = load_ratings_csv("imdbratings.csv", personal=False)
Personal_Ratings = load_ratings_csv("myratings.csv", personal=True)


# --- Debug: show column names ---
st.write("IMDB_Ratings columns:", IMDB_Ratings.columns.tolist())
st.write("Personal_Ratings columns:", Personal_Ratings.columns.tolist())


# --- Streamlit Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb & Personal Ratings Project 🎬")
st.write("Compare your personal ratings with IMDb ratings and explore the data.")


# --- IMDb Ratings Table ---
st.write("---")
st.write("### IMDb Ratings")
if not IMDB_Ratings.empty:
    min_rating = st.slider("Minimum IMDb rating:", 0, 10, 7, key="imdb_slider")
    filtered_imdb = IMDB_Ratings[IMDB_Ratings["imdb_rating"].astype(float) >= min_rating].sort_values("imdb_rating", ascending=False)
    st.dataframe(filtered_imdb, width="stretch", height=400)
else:
    st.warning("IMDb Ratings CSV is empty or failed to load.")


# --- Personal Ratings Table ---
st.write("---")
st.write("### Personal Ratings")
if not Personal_Ratings.empty:
    min_personal_rating = st.slider("Minimum Personal rating:", 0, 10, 7, key="personal_slider")
    filtered_personal = Personal_Ratings[Personal_Ratings["personal_ratings"].astype(float) >= min_personal_rating].sort_values("personal_ratings", ascending=False)
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
        # Convert ratings to float for calculations
        if "personal_ratings" in Personal_Ratings.columns:
            Personal_Ratings["personal_ratings"] = Personal_Ratings["personal_ratings"].astype(float)
        if "imdb_rating" in IMDB_Ratings.columns:
            IMDB_Ratings["imdb_rating"] = IMDB_Ratings["imdb_rating"].astype(float)

        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"SQL Error: {e}")
