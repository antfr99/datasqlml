import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb & My Ratings Project 🎬")
st.write("""
This project combines Streamlit, Pandas, PandasQL, and SQL queries to explore IMDb and your personal ratings.
""")

# --- Load Excel files ---
try:
    IMDB_Ratings = pd.read_excel("imdbratings.xlsx")
    My_Ratings = pd.read_excel("myratings.xlsx")
except Exception as e:
    st.error(f"Error loading Excel files: {e}")
    IMDB_Ratings = pd.DataFrame()
    My_Ratings = pd.DataFrame()

# --- Remove empty / unnamed columns ---
def clean_unnamed_columns(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

IMDB_Ratings = clean_unnamed_columns(IMDB_Ratings)
My_Ratings = clean_unnamed_columns(My_Ratings)

# --- Convert object columns to string for Streamlit display ---
def safe_for_streamlit(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].dtype == 'object':
            df_copy[col] = df_copy[col].astype(str)
    return df_copy

IMDB_Display = safe_for_streamlit(IMDB_Ratings)
My_Display = safe_for_streamlit(My_Ratings)

# --- Display Tables ---
st.write("---")
st.write("### IMDb Ratings Table")
if not IMDB_Ratings.empty:
    st.dataframe(IMDB_Display, width="stretch", height=400)
else:
    st.warning("IMDb Ratings Excel file is empty or failed to load.")

st.write("---")
st.write("### My Ratings Table")
if not My_Ratings.empty:
    st.dataframe(My_Display, width="stretch", height=400)
else:
    st.warning("My Ratings Excel file is empty or failed to load.")

# --- SQL Playground ---
st.write("---")
st.header("Try SQL Queries on IMDb Ratings and My Film Ratings")
st.write("""
Type any SQL query against either `IMDB_Ratings` or `My_Ratings`.

Example 1: `SELECT Title, [IMDb Rating] FROM IMDB_Ratings WHERE [IMDb Rating] > 8`  
Example 2: `SELECT Title, [Your Rating] FROM My_Ratings WHERE [Your Rating] >= 7`
""")

default_query = """SELECT pr.Title,
       pr.[Your Rating],
       ir.[IMDb Rating],
       ABS(pr.[Your Rating] - ir.[IMDb Rating]) AS Rating_Diff
FROM My_Ratings pr
JOIN IMDB_Ratings ir
    ON pr.[Movie ID] = ir.[Movie ID]
WHERE ABS(pr.[Your Rating] - ir.[IMDb Rating]) > 2
ORDER BY Rating_Diff DESC
LIMIT 10;"""

user_query = st.text_area(
    "Enter SQL query for either table:",
    default_query,
    key="sql_playground",
    height=300
)

if st.button("Run SQL Query"):
    try:
        # Convert numeric columns to float for calculations
        numeric_cols_my = ["Your Rating"]
        numeric_cols_imdb = ["IMDb Rating"]

        for col in numeric_cols_my:
            if col in My_Ratings.columns:
                My_Ratings[col] = pd.to_numeric(My_Ratings[col], errors='coerce')
        for col in numeric_cols_imdb:
            if col in IMDB_Ratings.columns:
                IMDB_Ratings[col] = pd.to_numeric(IMDB_Ratings[col], errors='coerce')

        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error in SQL query: {e}")
