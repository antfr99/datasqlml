import streamlit as st
import pandas as pd
import pandasql as ps

# --- Robust CSV loader ---
def load_ratings_csv(file_path, personal=False):
    """
    Robust loader for ratings CSV files.
    Args:
        file_path (str): Path to the CSV file
        personal (bool): If True, renames 'Your Rating' to 'Personal Ratings'
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    try:
        df = pd.read_csv(
            file_path,
            encoding='utf-8-sig',
            quotechar='"',
            skip_blank_lines=True,
            on_bad_lines='skip'
        )
        df.columns = df.columns.str.strip()
        
        # Rename columns
        if personal and "Your Rating" in df.columns:
            df = df.rename(columns={"Your Rating": "Personal Ratings"})
        if "Const" in df.columns:
            df = df.rename(columns={"Const": "Movie ID"})
        
        # Clean Director column
        if "Director" in df.columns:
            df["Director"] = df["Director"].fillna("").apply(
                lambda x: x.split(",")[0].strip() if x else None
            )
        
        # Clean Genre column
        if "Genre" in df.columns:
            df["Genre"] = df["Genre"].fillna("").apply(
                lambda x: x.split(",")[0].strip() if x else None
            )
        
        df = df.reset_index(drop=True)
        return df
    
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return pd.DataFrame()


# --- Load CSVs ---
IMDB_Ratings = load_ratings_csv("imdbratings.csv", personal=False)
Personal_Ratings = load_ratings_csv("myratings.csv", personal=True)


# --- Streamlit Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb & Personal Ratings Project 🎬")
st.write("""
Explore your movies interactively and compare personal ratings vs IMDb ratings. 
Use SQL queries to analyze the data.
""")


# --- IMDb Ratings Table ---
st.write("---")
st.write("### IMDb Ratings")
if not IMDB_Ratings.empty:
    min_rating = st.slider("Minimum IMDb rating to display:", 0, 10, 7, key="imdb_slider")
    filtered_imdb = IMDB_Ratings[IMDB_Ratings["IMDb Rating"] >= min_rating].sort_values("IMDb Rating", ascending=False)
    st.dataframe(filtered_imdb, width="stretch", height=400)
else:
    st.warning("IMDb Ratings CSV is empty or failed to load.")


# --- Personal Ratings Table ---
st.write("---")
st.write("### Personal Ratings")
if not Personal_Ratings.empty:
    min_personal_rating = st.slider("Minimum Personal rating to display:", 0, 10, 7, key="personal_slider")
    filtered_personal = Personal_Ratings[Personal_Ratings["Personal Ratings"] >= min_personal_rating].sort_values("Personal Ratings", ascending=False)
    st.dataframe(filtered_personal, width="stretch", height=400)
else:
    st.warning("Personal Ratings CSV is empty or failed to load.")


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
