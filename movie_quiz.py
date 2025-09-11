import streamlit as st
import pandas as pd
import pandasql as ps

# --- Load .xlsx files ---
try:
    IMDB_Ratings = pd.read_excel("imdbratings.xlsx")
    Personal_Ratings = pd.read_excel("myratings.xlsx")
except Exception as e:
    st.error(f"Error loading Excel files: {e}")
    IMDB_Ratings = pd.DataFrame()
    Personal_Ratings = pd.DataFrame()

# --- Remove empty/unnamed columns ---
def clean_unnamed_columns(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

IMDB_Ratings = clean_unnamed_columns(IMDB_Ratings)
Personal_Ratings = clean_unnamed_columns(Personal_Ratings)

# --- Streamlit Page ---
st.set_page_config(layout="wide")
st.title("IMDb & Personal Ratings - Raw Tables")

# --- Show IMDb Ratings ---
st.write("---")
st.write("### IMDb Ratings Table")
if not IMDB_Ratings.empty:
    st.dataframe(IMDB_Ratings, width="stretch", height=400)
else:
    st.warning("IMDb Ratings Excel file is empty or failed to load.")

# --- Show Personal Ratings ---
st.write("---")
st.write("### My Ratings Table")
if not Personal_Ratings.empty:
    st.dataframe(Personal_Ratings, width="stretch", height=400)
else:
    st.warning("Personal Ratings Excel file is empty or failed to load.")

# --- Single SQL Playground for both tables ---
st.write("---")
st.header("Try SQL Queries on IMDb Ratings and My Personal Film Ratings")
st.write(
    """
Type any SQL query against either `IMDB_Ratings` or `Personal_Ratings`.

Example 1: `SELECT Title, [IMDb Rating] FROM IMDB_Ratings WHERE [IMDb Rating] > 8`  
Example 2: `SELECT Title, [Your Rating] FROM Personal_Ratings WHERE [Your Rating] >= 7`
"""
)

default_query = """SELECT pr.Title,
       pr.[Your Rating],
       ir.[IMDb Rating],
       ABS(pr.[Your Rating] - ir.[IMDb Rating]) AS Rating_Diff
FROM Personal_Ratings pr
JOIN IMDB_Ratings ir
    ON pr.[Movie ID] = ir.[Movie ID]
WHERE ABS(pr.[Your Rating] - ir.[IMDb Rating]) > 2
ORDER BY Rating_Diff DESC
LIMIT 10;"""

user_query = st.text_area("Enter SQL query for either table:", default_query, height=300, key="sql_playground")

if st.button("Run SQL Query"):
    try:
        # Ensure numeric columns are floats for calculation
        if "Your Rating" in Personal_Ratings.columns:
            Personal_Ratings["Your Rating"] = Personal_Ratings["Your Rating"].astype(float)
        if "IMDb Rating" in IMDB_Ratings.columns:
            IMDB_Ratings["IMDb Rating"] = IMDB_Ratings["IMDb Rating"].astype(float)

        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error in SQL query: {e}")
