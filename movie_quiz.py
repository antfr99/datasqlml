import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb/SQL Data Project 🎬")

st.write("""
This is a small imdb data project combining Python Packages ( Streamlit, Pandas , PandasQL ), ChatGPT, SQL, GitHub, and Streamlit.
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
# --- Scenario 1 ---
st.header("Scenario 1: Rating Differences")
scenario1_query = """SELECT pr.Title,
       pr.[Your Rating],
       ir.[IMDb Rating],
       ABS(CAST(pr.[Your Rating] AS FLOAT) - CAST(ir.[IMDb Rating] AS FLOAT)) AS Rating_Diff
FROM My_Ratings pr
JOIN IMDB_Ratings ir
    ON pr.[Movie ID] = ir.[Movie ID]
WHERE ABS(CAST(pr.[Your Rating] AS FLOAT) - CAST(ir.[IMDb Rating] AS FLOAT)) > 2
ORDER BY Rating_Diff DESC
LIMIT 10;"""

if st.button("Run Scenario 1 SQL"):
    try:
        result1 = ps.sqldf(scenario1_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
        st.dataframe(result1, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error running Scenario 1 SQL: {e}")

# --- Scenario 2 ---
st.header("Scenario 2: Hybrid Recommendations")
scenario2_query = """SELECT ir.Title,
       1.0 * (CASE WHEN ir.Director IN (SELECT DISTINCT Director FROM My_Ratings WHERE [Your Rating] >= 7) THEN 1 ELSE 0 END)
       + (CASE WHEN ir.Genre IN ('Comedy', 'Drama') THEN 0.5 ELSE 0.2 END) AS Recommendation_Score
FROM IMDB_Ratings ir
LEFT JOIN My_Ratings mr
    ON ir.[Movie ID] = mr.[Movie ID]
WHERE mr.[Movie ID] IS NULL AND ir.[Num Votes] >= 30000
ORDER BY Recommendation_Score DESC
LIMIT 10;"""

if st.button("Run Scenario 2 SQL"):
    try:
        result2 = ps.sqldf(scenario2_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
        st.dataframe(result2, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error running Scenario 2 SQL: {e}")

# --- Scenario 3 ---
st.header("Scenario 3: Top Rated Yet Unseen")
scenario3_query = """SELECT ir.Title,
       ir.[IMDb Rating],
       ir.[Num Votes]
FROM IMDB_Ratings ir
LEFT JOIN My_Ratings mr
    ON ir.[Movie ID] = mr.[Movie ID]
WHERE mr.[Movie ID] IS NULL AND ir.[Num Votes] >= 30000
ORDER BY ir.[IMDb Rating] DESC
LIMIT 10;"""

if st.button("Run Scenario 3 SQL"):
    try:
        result3 = ps.sqldf(scenario3_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
        st.dataframe(result3, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error running Scenario 3 SQL: {e}")
