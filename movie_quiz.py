# --- Single SQL Playground for both tables ---
st.write("---")
st.header("Try SQL Queries on IMDb Ratings and My Film Ratings")
st.write("""
Type any SQL query against either `IMDB_Ratings` or `My_Ratings`.

**Scenario 1:**  
Imagine you want to find movies where your personal rating is very different from the IMDb rating.  
The following default query will show the top 10 movies where your rating and IMDb rating differ by more than 2 points, along with the absolute difference:

This helps you quickly spot movies you might have over- or underrated compared to IMDb.
""")

default_query_1 = """SELECT pr.Title,
       pr.[Your Rating],
       ir.[IMDb Rating],
       ABS(CAST(pr.[Your Rating] AS FLOAT) - CAST(ir.[IMDb Rating] AS FLOAT)) AS Rating_Diff
FROM My_Ratings pr
JOIN IMDB_Ratings ir
    ON pr.[Movie ID] = ir.[Movie ID]
WHERE ABS(CAST(pr.[Your Rating] AS FLOAT) - CAST(ir.[IMDb Rating] AS FLOAT)) > 2
ORDER BY Rating_Diff DESC
LIMIT 10;"""

st.write("""
**Scenario 2 (Hybrid Recommendation):**  
Imagine you want to get recommendations for films you haven't rated yet.  
- If you liked the director before → +1 point  
- If the genre is Comedy or Drama → +0.5  
- Otherwise → +0.2  

This helps you prioritize unseen movies you are likely to enjoy based on your past preferences.
""")

default_query_2 = """SELECT ir.Title,
       ir.Director,
       ir.Genre,
       CASE WHEN ir.Director IN (SELECT DISTINCT Director FROM My_Ratings WHERE [Your Rating] >= 7) THEN 1 ELSE 0 END
       + CASE WHEN ir.Genre IN ('Comedy','Drama') THEN 0.5 ELSE 0.2 END AS Recommendation_Score
FROM IMDB_Ratings ir
LEFT JOIN My_Ratings pr
    ON ir.[Movie ID] = pr.[Movie ID]
WHERE pr.[Your Rating] IS NULL
ORDER BY Recommendation_Score DESC
LIMIT 10;"""

st.write("""
**Scenario 3 (Top Rated Yet Unseen):**  
This scenario shows the top 10 highest IMDb rated films you haven’t rated yet.  
It’s a quick way to find highly-rated movies that are missing from your personal list.
""")

default_query_3 = """SELECT ir.Title,
       ir.[IMDb Rating],
       ir.Genre,
       ir.Director
FROM IMDB_Ratings ir
LEFT JOIN My_Ratings pr
    ON ir.[Movie ID] = pr.[Movie ID]
WHERE pr.[Your Rating] IS NULL
ORDER BY ir.[IMDb Rating] DESC
LIMIT 10;"""

# --- Select Scenario ---
scenario = st.radio("Choose a scenario:", ["Scenario 1", "Scenario 2", "Scenario 3"])

query_map = {
    "Scenario 1": default_query_1,
    "Scenario 2": default_query_2,
    "Scenario 3": default_query_3
}

user_query = st.text_area(
    "Enter SQL query for selected scenario:",
    query_map[scenario],
    height=300,
    key="sql_playground"
)

if st.button("Run SQL Query"):
    try:
        result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_safe, "My_Ratings": My_safe})
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error in SQL query: {e}")
