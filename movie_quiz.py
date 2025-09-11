import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Project Description ---
st.title("IMDb/SQL Data Project 🎬")
st.write(
    """
This is a small imdb data project combining Python Packages ( Streamlit, Pandas , PandasQL ), ChatGPT, SQL, GitHub, and Streamlit.
"""
)

# --- Load .xlsx files ---

# --- Load Excel files ---
try:
    IMDB_Ratings = pd.read_excel("imdbratings.xlsx")
    My_Ratings = pd.read_excel("myratings.xlsx")
except Exception as e:
    st.error(f"Error loading Excel files: {e}")
    IMDB_Ratings = pd.DataFrame()
    My_Ratings = pd.DataFrame()

# --- Remove empty/unnamed columns ---
def clean_unnamed_columns(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

IMDB_Ratings = clean_unnamed_columns(IMDB_Ratings)
My_Ratings = clean_unnamed_columns(My_Ratings)

# --- Drop columns with unsupported types for SQL ---
def prepare_for_sql(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if pd.api.types.is_datetime64_any_dtype(df_copy[col]) or pd.api.types.is_timedelta64_dtype(df_copy[col]):
            df_copy[col] = df_copy[col].astype(str)
    return df_copy

IMDB_SQL = prepare_for_sql(IMDB_Ratings)
My_SQL = prepare_for_sql(My_Ratings)

# --- Show tables ---
st.write("### IMDb Ratings Table")
st.dataframe(IMDB_Ratings)

st.write("### My Ratings Table")
st.dataframe(My_Ratings)

# --- SQL Playground ---
st.write("---")
st.header("Try SQL Queries on IMDb Ratings and My Film Ratings")

default_query = """SELECT pr.Title,
       pr.[Your Rating],
       ir.[IMDb Rating],
       ABS(pr.[Your Rating] - ir.[IMDb Rating]) AS Rating_Diff
FROM My_SQL pr
JOIN IMDB_SQL ir
    ON pr.[Movie ID] = ir.[Movie ID]
WHERE ABS(pr.[Your Rating] - ir.[IMDb Rating]) > 2
ORDER BY Rating_Diff DESC
LIMIT 10;"""

user_query = st.text_area("Enter SQL query:", default_query, height=300)

if st.button("Run SQL Query"):
    try:
        # Convert numeric columns to float
        if "Your Rating" in My_SQL.columns:
            My_SQL["Your Rating"] = pd.to_numeric(My_SQL["Your Rating"], errors='coerce')
        if "IMDb Rating" in IMDB_SQL.columns:
            IMDB_SQL["IMDb Rating"] = pd.to_numeric(IMDB_SQL["IMDb Rating"], errors='coerce')

        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"SQL Error: {e}")