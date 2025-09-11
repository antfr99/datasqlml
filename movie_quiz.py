import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Project Description ---
st.title("IMDb/SQL Data Project 🎬")
st.write("""
This is a small IMDb data project combining Python Packages (Streamlit, Pandas, PandasQL), ChatGPT, SQL, GitHub, and Streamlit.
""")

# --- Load .xlsx files ---
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

# --- Convert all columns to SQLite-safe types ---
def make_sqlite_safe(df):
    df_safe = df.copy()
    for col in df_safe.columns:
        # Numeric columns
        if pd.api.types.is_numeric_dtype(df_safe[col]):
            df_safe[col] = pd.to_numeric(df_safe[col], errors='coerce')
        # Datetime/Timedelta columns → string
        elif pd.api.types.is_datetime64_any_dtype(df_safe[col]) or pd.api.types.is_timedelta64_dtype(df_safe[col]):
            df_safe[col] = df_safe[col].astype(str)
        # All other objects → string
        else:
            df_safe[col] = df_safe[col].astype(str)
    return df_safe

IMDB_safe = make_sqlite_safe(IMDB_Ratings)
My_safe = make_sqlite_safe(My_Ratings)

# --- Show IMDb Ratings ---
st.write("---")
st.write("### IMDb Ratings Table")
if not IMDB_Ratings.empty:
    st.dataframe(IMDB_Ratings, width="stretch", height=400)
else:
    st.warning("IMDb Ratings Excel file is empty or failed to load.")

# --- Show My Ratings ---
st.write("---")
st.write("### My Ratings Table")
if not My_Ratings.empty:
    st.dataframe(My_Ratings, width="stretch", height=400)
else:
    st.warning("My Ratings Excel file is empty or failed to load.")

# --- Single SQL Playground for both tables ---
st.write("---")
st.header("Try SQL Queries on IMDb Ratings and My Film Ratings")
st.write("""
Type any SQL query against either `IMDB_Ratings` or `My_Ratings`.

**Scenario Example:**  
Imagine you want to find movies where your personal rating is very different from the IMDb rating.  
The following default query will show the top 10 movies where your rating and IMDb rating differ by more than 2 points, along with the absolute difference:

This helps you quickly spot movies you might have over- or underrated compared to IMDb.
""")

default_query = """SELECT pr.Title,
       pr.[Your Rating],
       ir.[IMDb Rating],
       ABS(CAST(pr.[Your Rating] AS FLOAT) - CAST(ir.[IMDb Rating] AS FLOAT)) AS Rating_Diff
FROM My_Ratings pr
JOIN IMDB_Ratings ir
    ON pr.[Movie ID] = ir.[Movie ID]
WHERE ABS(CAST(pr.[Your Rating] AS FLOAT) - CAST(ir.[IMDb Rating] AS FLOAT)) > 2
ORDER BY Rating_Diff DESC
LIMIT 10;"""

user_query = st.text_area(
    "Enter SQL query for either table:",
    default_query,
    height=300,
    key="sql_playground"
)

if st.button("Run SQL Query"):
    try:
        result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_safe, "My_Ratings": My_safe})
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error in SQL query: {e}")
