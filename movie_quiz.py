import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb/SQL Data Project 🎬")

st.write("""
This project combines Streamlit, Pandas, PandasQL, and SQL to explore IMDb and personal movie ratings data.
""")

# --- Load Excel files ---
try:
    IMDB_Ratings = pd.read_excel("imdbratings.xlsx")
    My_Ratings = pd.read_excel("myratings.xlsx")
    Votes = pd.read_excel("votes.xlsx")  # New votes source
except Exception as e:
    st.error(f"Error loading Excel files: {e}")
    IMDB_Ratings = pd.DataFrame()
    My_Ratings = pd.DataFrame()
    Votes = pd.DataFrame()

# --- Remove empty/unnamed columns ---
def clean_unnamed_columns(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

IMDB_Ratings = clean_unnamed_columns(IMDB_Ratings)
My_Ratings = clean_unnamed_columns(My_Ratings)
Votes = clean_unnamed_columns(Votes)

# --- Merge votes into IMDB_Ratings ---
if not Votes.empty:
    IMDB_Ratings = IMDB_Ratings.merge(Votes, on="Movie ID", how="left")

# --- Show Tables ---
st.write("---")
st.write("### IMDb Ratings Table")
if not IMDB_Ratings.empty:
    st.dataframe(IMDB_Ratings, width="stretch", height=400)
else:
    st.warning("IMDb Ratings Excel file is empty or failed to load.")

st.write("---")
st.write("### My Ratings Table")
if not My_Ratings.empty:
    st.dataframe(My_Ratings, width="stretch", height=400)
else:
    st.warning("My Ratings Excel file is empty or failed to load.")

# --- SQL Playground ---
st.write("---")
st.header("Try SQL Queries on IMDb Ratings and My Film Ratings")
st.write("""
Type any SQL query against either `IMDB_Ratings` or `My_Ratings`.

**Scenario 1:**  
Find movies where your personal rating is very different from the IMDb rating.  
This query shows the top 10 movies where your rating differs from IMDb by more than 2 points:

**Scenario 2 (Hybrid Recommendations):**  
Recommend movies you haven’t rated yet:  
- Add 1 point if you liked the director before  
- Add 0.5 if genre is Comedy/Drama, otherwise 0.2  
Only consider movies with at least 30,000 votes.

**Scenario 3 (Top Rated Yet Unseen):**  
Shows the top-rated movies on IMDb you haven’t seen yet, again only movies with at least 30,000 votes.
""")

# --- Default SQL Query for Scenario 1 ---
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
        # Ensure numeric columns are floats for calculations
        if "Your Rating" in My_Ratings.columns:
            My_Ratings["Your Rating"] = My_Ratings["Your Rating"].astype(float)
        if "IMDb Rating" in IMDB_Ratings.columns:
            IMDB_Ratings["IMDb Rating"] = IMDB_Ratings["IMDb Rating"].astype(float)
        if "Num Votes" in IMDB_Ratings.columns:
            IMDB_Ratings["Num Votes"] = IMDB_Ratings["Num Votes"].astype(float)

        # Use safe copies for SQL queries
        IMDB_safe = IMDB_Ratings.copy()
        My_safe = My_Ratings.copy()

        result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_safe, "My_Ratings": My_safe})
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error in SQL query: {e}")
