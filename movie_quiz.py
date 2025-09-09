import streamlit as st
import pandas as pd
import pandasql as ps

# --- Load Movies CSV ---
movies_df = pd.read_csv("movies.csv")
movies_df.columns = movies_df.columns.str.strip()

# --- Clean IMDB_Ratings for quiz and IMDb filter ---
IMDB_Ratings = movies_df.copy()

# 2️⃣ Rename 'Const' to 'Movie ID'
if "Const" in IMDB_Ratings.columns:
    IMDB_Ratings = IMDB_Ratings.rename(columns={"Const": "Movie ID"})

# 3️⃣ Remove unnecessary columns
cols_to_drop = ["Your Rating", "Date Rated", "Original Title", "URL"]
IMDB_Ratings = IMDB_Ratings.drop(columns=[c for c in cols_to_drop if c in IMDB_Ratings.columns])

# 4️⃣ Keep only the first director per movie and rename to 'director'
if "Directors" in IMDB_Ratings.columns:
    IMDB_Ratings["director"] = IMDB_Ratings["Directors"].fillna("").apply(
        lambda x: x.split(",")[0].strip() if x else ""
    )
    IMDB_Ratings = IMDB_Ratings.drop(columns=["Directors"])

IMDB_Ratings = IMDB_Ratings.reset_index(drop=True)

# 4️⃣ Keep only the first director per movie and rename to 'director'
if "Directors" in IMDB_Ratings.columns:
    IMDB_Ratings["director"] = IMDB_Ratings["Directors"].fillna("").apply(
        lambda x: x.split(",")[0].strip() if x else ""
    )
    IMDB_Ratings = IMDB_Ratings.drop(columns=["Directors"])

# ✅ Clean director column (remove blanks, placeholders, normalize)
bad_tokens = {"", "nan", "none", "null", "n/a", "unknown"}
IMDB_Ratings["director"] = (
    IMDB_Ratings["director"]
    .astype(str)
    .str.strip()
    .replace(bad_tokens, None)   # replace bad tokens with real None/NaN
)

# --- Create Personal Ratings table ---
Personal_Ratings = movies_df.copy()

# Keep only the first director and rename column
if "Directors" in Personal_Ratings.columns:
    Personal_Ratings["Director"] = Personal_Ratings["Directors"].fillna("").apply(
        lambda x: x.split(",")[0].strip() if x else ""
    )

# Rename columns
rename_map = {
    "Const": "Movie ID",
    "Your Rating": "Personal Ratings"
}
Personal_Ratings = Personal_Ratings.rename(columns=rename_map)

# Keep only desired columns
desired_cols = [
    "Movie ID", "Personal Ratings", "Date Rated", "Title", "URL",
    "Title Type", "Runtime (mins)", "Year",
    "Release Date", "Director", "Genre"  # keep Genre for SQL
]
Personal_Ratings = Personal_Ratings[[c for c in desired_cols if c in Personal_Ratings.columns]]
Personal_Ratings = Personal_Ratings.reset_index(drop=True)

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Project Description ---
st.title("Movie SQL Sandbox & SQL Quiz 🎬")
st.write(
    """
This is a small personal project combining **Python, SQL, IMDb, GitHub, and Streamlit** which provides a SQL Sandbox and also tests your SQL knowledge.
"""
)

# --- Single SQL Playground for both tables ---
st.write("---")
st.header("Try SQL Queries on IMDB Ratings and my Personal Film Ratings")
st.write(
    """
Type any SQL query against either `IMDB_Ratings` or `Personal_Ratings`.

Example 1: `SELECT Title, [IMDb Rating] FROM IMDB_Ratings WHERE [IMDb Rating] > 8`  
Example 2: `SELECT Title, [Personal Ratings] FROM Personal_Ratings WHERE [Personal Ratings] >= 7`
"""
)


user_query = st.text_area(
    "Enter SQL query for either table:",
    "SELECT * FROM IMDB_Ratings LIMIT 5",
    key="sql_playground"
)

if st.button("Run SQL Query"):
    try:
        # Both tables are available in locals()
        result = ps.sqldf(user_query, locals())
        st.dataframe(result, width="stretch", height=400)
    except Exception as e:
        st.error(f"Error in SQL query: {e}")

# --- Explore movies by IMDb rating ---        

st.write("---")
st.write("### IMDb Ratings > Movies I’ve seen, sorted by IMDb rating")
min_rating = st.slider(
    "Show movies with IMDb rating at least:",
    0, 10, 7,
    key="imdb_slider"
)
filtered_movies = IMDB_Ratings[IMDB_Ratings["IMDb Rating"] >= min_rating].sort_values("IMDb Rating", ascending=False)

# Drop Genre only for display
st.dataframe(
    filtered_movies.drop(columns=["Genres"], errors="ignore"),
    width="stretch",
    height=400
)

# --- Personal Ratings Table ---
# --- Personal Ratings Table ---
st.write("---")
st.write("### Personal Ratings")

# 🎛️ Add a slider filter for Personal Ratings
min_personal_rating = st.slider(
    "Show movies with Personal rating at least:",
    0, 10, 7,
    key="personal_slider"
)

filtered_personal = Personal_Ratings[
    Personal_Ratings["Personal Ratings"] >= min_personal_rating
].sort_values("Personal Ratings", ascending=False)

st.dataframe(
    filtered_personal.drop(columns=["Genre"], errors="ignore"),
    width="stretch",
    height=400
)

# =====================
# SQL QUIZ
# =====================

# =====================
# SQL QUIZ
# =====================
import streamlit as st
import pandas as pd
import pandasql as ps

# ================= Q1 =================
st.write("**Q1.** List the top 10 movies where Personal rating differs from IMDb rating by more than 2 points, ordered by difference descending.")

sql_options1 = [
    """SELECT Title,
              [Personal Ratings],
              [IMDb Rating]
       FROM Personal_Ratings
       WHERE [Personal Ratings] - [IMDb Rating] > 2
       ORDER BY [Personal Ratings] DESC
       LIMIT 10;""",

    """SELECT pr.Title,
              pr.[Personal Ratings],
              ir.[IMDb Rating],
              ABS(pr.[Personal Ratings] - ir.[IMDb Rating]) AS Rating_Diff
       FROM Personal_Ratings pr
       JOIN IMDB_Ratings ir 
           ON pr.[Movie ID] = ir.[Movie ID]
       WHERE ABS(pr.[Personal Ratings] - ir.[IMDb Rating]) > 2
       ORDER BY Rating_Diff DESC
       LIMIT 10;""",  # ✅ correct

    """SELECT pr.Title,
              pr.[Personal Ratings],
              ir.[IMDb Rating],
              ABS(pr.[Personal Ratings] - ir.[IMDb Rating]) AS Rating_Diff
       FROM Personal_Ratings pr
       JOIN IMDB_Ratings ir 
           ON pr.[Movie ID] = ir.[Movie ID]
       ORDER BY Rating_Diff ASC
       LIMIT 10;"""  # ❌ incorrect
]

labels1 = ["Option 1", "Option 2", "Option 3"]

selected_index1 = st.radio(
    "Select your answer:", 
    options=[None, 0, 1, 2], 
    format_func=lambda x: "Select an Option" if x is None else labels1[x],
    key="q1_radio"
)

for i, sql in enumerate(sql_options1):
    st.markdown(f"**{labels1[i]}**")
    st.code(sql, language="sql")

if selected_index1 is not None:
    if selected_index1 == 1:
        st.success("✅ Correct!")
        result_q1 = ps.sqldf(sql_options1[selected_index1], locals())
        st.dataframe(result_q1, width="stretch", height=400)
        st.markdown("""
**Explanation:**
1️⃣ Option 1 is incorrect because it does not join with IMDB_Ratings.  
3️⃣ Option 3 is incorrect because it orders ascending instead of descending.
""")
    else:
        st.error("❌ Try again.")

# ================= Q2 =================
st.write("---")
st.write("**Q2.** Find the highest-rated movie for each year (IMDb rating) and order by year ascending.")

sql_options2 = [
    """SELECT ir.Year,
              ir.Title,
              ir.[IMDb Rating]
       FROM IMDB_Ratings ir
       GROUP BY ir.Year;""",  # ❌ Incorrect

    """SELECT ir.Year,
              ir.Title,
              ir.[IMDb Rating]
       FROM IMDB_Ratings ir
       ORDER BY ir.Year ASC;""",  # ❌ Incorrect

    """SELECT ir1.Year,
              ir1.Title,
              ir1.[IMDb Rating]
       FROM IMDB_Ratings ir1
       WHERE ir1.[IMDb Rating] = (
           SELECT MAX(ir2.[IMDb Rating])
           FROM IMDB_Ratings ir2
           WHERE ir2.Year = ir1.Year
       )
       ORDER BY ir1.Year ASC;"""  # ✅ Correct
]

labels2 = ["Option 1", "Option 2", "Option 3"]

selected_index2 = st.radio(
    "Select your answer:", 
    options=[None, 0, 1, 2],
    format_func=lambda x: "Select an Option" if x is None else labels2[x],
    key="q2_radio"
)

for i, sql in enumerate(sql_options2):
    st.markdown(f"**{labels2[i]}**")
    st.code(sql, language="sql")

if selected_index2 is not None:
    if selected_index2 == 2:
        st.success("✅ Correct!")
        result_q2 = ps.sqldf(sql_options2[selected_index2], locals())
        st.dataframe(result_q2, width="stretch", height=400)
        st.markdown("""
**Explanation:**
1️⃣ Option 1** is incorrect because it groups only by `Year` without aggregating `Title` or `IMDb Rating`. This either causes an SQL error or returns arbitrary movies per year.   
2️⃣ Option 2 is incorrect because it does not select the maximum rating per year.
""")
    else:
        st.error("❌ Try again.")


# ================= Q3 =================
st.write("---")
st.write("**Q3.** Show top 10 personal rated movies by difference from IMDb, descending.")

sql_options3 = [
    """SELECT pr.Title,
              pr.[Personal Ratings],
              ir.[IMDb Rating],
              (pr.[Personal Ratings] - ir.[IMDb Rating]) AS Diff
       FROM Personal_Ratings pr
       JOIN IMDB_Ratings ir ON pr.[Movie ID] = ir.[Movie ID]
       ORDER BY Diff DESC
       LIMIT 10;""",  # ✅ correct

    """SELECT pr.Title,
              pr.[Personal Ratings],
              ir.[IMDb Rating]
       FROM Personal_Ratings pr
       JOIN IMDB_Ratings ir ON pr.[Movie ID] = ir.[Movie ID]
       ORDER BY Diff DESC
       LIMIT 10;""",  # ❌ Incorrect

    """SELECT pr.Title,
              pr.[Personal Ratings],
              ir.[IMDb Rating],
              (pr.[Personal Ratings] - ir.[IMDb Rating]) AS Diff
       FROM Personal_Ratings pr
       JOIN IMDB_Ratings ir ON pr.[Movie ID] = ir.[Movie ID]
       ORDER BY Diff ASC
       LIMIT 10;"""  # ❌ Incorrect
]

labels3 = ["Option 1", "Option 2", "Option 3"]

selected_index3 = st.radio(
    "Select your answer:", 
    options=[None, 0, 1, 2],
    format_func=lambda x: "Select an Option" if x is None else labels3[x],
    key="q3_radio"
)

for i, sql in enumerate(sql_options3):
    st.markdown(f"**{labels3[i]}**")
    st.code(sql, language="sql")

if selected_index3 is not None:
    if selected_index3 == 0:
        st.success("✅ Correct!")
        result_q3 = ps.sqldf(sql_options3[selected_index3], locals())
        st.dataframe(result_q3, width="stretch", height=400)
        st.markdown("""
**Explanation:**
2️⃣ Option 2 is incorrect because Diff is not defined.  
3️⃣ Option 3 is incorrect because ASC orders smallest difference first.
""")
    else:
        st.error("❌ Try again.")

# ================= Q4 =================
st.write("---")
st.write("**Q4.** Find top 10 movie pairs by the same director with largest IMDb rating difference.")

sql_options4 = [
    """SELECT ir1.director,
              ir1.Title
       FROM IMDB_Ratings ir1;""",  # ❌ Incorrect

    """SELECT ir1.director,
              ir1.Title AS Movie1,
              ir2.Title AS Movie2,
              ABS(ir1.[IMDb Rating] - ir2.[IMDb Rating]) AS Rating_Diff
       FROM IMDB_Ratings ir1
       JOIN IMDB_Ratings ir2
         ON ir1.director = ir2.director
        AND ir1.[Movie ID] < ir2.[Movie ID]
       ORDER BY Rating_Diff DESC
       LIMIT 10;""",  # ✅ Correct

    """SELECT ir1.director,
              ir1.Title AS Movie1,
              ir2.Title AS Movie2,
              ABS(ir1.[IMDb Rating] - ir2.[IMDb Rating]) AS Rating_Diff
       FROM IMDB_Ratings ir1
       JOIN IMDB_Ratings ir2
         ON ir1.director = ir2.director
         ORDER BY Rating_Diff ASC
       LIMIT 10;"""  # ❌ Incorrect
]

labels4 = ["Option 1", "Option 2", "Option 3"]

selected_index4 = st.radio(
    "Select your answer:", 
    options=[None, 0, 1, 2],
    format_func=lambda x: "Select an Option" if x is None else labels4[x],
    key="q4_radio"
)

for i, sql in enumerate(sql_options4):
    st.markdown(f"**{labels4[i]}**")
    st.code(sql, language="sql")

if selected_index4 is not None:
    if selected_index4 == 1:
        st.success("✅ Correct!")
        result_q4 = ps.sqldf(sql_options4[selected_index4], locals())
        st.dataframe(result_q4, width="stretch", height=400)
        st.markdown("""
**Explanation:**
1️⃣ Option 1 is incorrect because the query does nothing useful.  
3️⃣ Option 3 is incorrect because ASC and missing ID filter create duplicates.  

""")
    else:
        st.error("❌ Try again.")


# ================= Q5 =================
st.write("---")
st.write("**Q5.** Find movies released in the same year with identical runtime (self-join).")

sql_options5 = [
    """SELECT ir1.Title,
              ir1.Year,
              ir1.[Runtime (mins)]
       FROM IMDB_Ratings ir1;""",  # ❌ Incorrect

    """SELECT ir1.Title AS Movie1,
              ir2.Title AS Movie2,
              ir1.Year,
              ir1.[Runtime (mins)] AS "Runtime (mins)"
       FROM IMDB_Ratings ir1
       JOIN IMDB_Ratings ir2
         ON ir1.Year = ir2.Year
        AND ir1.[Runtime (mins)] = ir2.[Runtime (mins)]
        AND ir1.[Movie ID] < ir2.[Movie ID]
       ORDER BY ir1.Year DESC,
                ir1.[Runtime (mins)] DESC
       LIMIT 10;""",  # ✅ Correct

    """SELECT ir1.Title AS Movie1,
              ir2.Title AS Movie2,
              ir1.Year,
              ir1.[Runtime (mins)]
       FROM IMDB_Ratings ir1
       JOIN IMDB_Ratings ir2
         ON ir1.Year = ir2.Year
       ORDER BY ir1.Year DESC
       LIMIT 10;"""  # ❌ Incorrect
]

labels5 = ["Option 1", "Option 2", "Option 3"]

selected_index5 = st.radio(
    "Select your answer:", 
    options=[None, 0, 1, 2],
    format_func=lambda x: "Select an Option" if x is None else labels5[x],
    key="q5_radio"
)

for i, sql in enumerate(sql_options5):
    st.markdown(f"**{labels5[i]}**")
    st.code(sql, language="sql")

if selected_index5 is not None:
    if selected_index5 == 1:
        st.success("✅ Correct!")
        result_q5 = ps.sqldf(sql_options5[selected_index5], locals())
        st.dataframe(result_q5, width="stretch", height=400)
        st.markdown("""
**Explanation:**
1️⃣ Option 1 is incorrect because query does not pair movies correctly (no self-join logic).  
3️⃣ Option 3 is incorrect because it only matches on year, not runtime, and allows duplicates.  

""")
    else:
        st.error("❌ Try again.")

# ============================
# --- Load & Combine Other Ratings ---
# ============================

others1 = pd.read_csv("othersratings1.csv")
others2 = pd.read_csv("othersratings2.csv")

# Standardize columns
for df in [others1, others2]:
    df.columns = df.columns.str.strip()
    df.rename(columns={"Const": "Movie ID"}, inplace=True)
    if "Directors" in df.columns:
        df["Director"] = df["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
        df.drop(columns=["Directors"], inplace=True)

# Keep only desired columns
desired_cols = [
    "Movie ID", "IMDb Rating", "Date Rated", "Title", "URL",
    "Title Type", "Runtime (mins)", "Year",
    "Release Date", "Director", "Genre"
]

others_combined = pd.concat([others1, others2], ignore_index=True)
others_combined = others_combined[[c for c in desired_cols if c in others_combined.columns]]
others_combined = others_combined.drop_duplicates(subset=["Movie ID"])

# --- Display Combined Other Ratings ---
st.write("---")
st.write("### IMDB Ratings Table 2")

min_other_rating = st.slider(
    "Show movies with rating at least:",
    0, 10, 7,
    key="other_slider"
)

filtered_others = others_combined[
    others_combined["IMDb Ratings"] >= min_other_rating
].sort_values("IMDb Rating", ascending=False)

st.dataframe(
    filtered_others.drop(columns=["Genre"], errors="ignore"),
    width="stretch",
    height=400
)

# ============================
# --- Load My Ratings CSV ---
# ============================

myratings = pd.read_csv("myratings.csv")
myratings.columns = myratings.columns.str.strip()
myratings.rename(columns={"Const": "Movie ID", "Your Rating": "Personal Ratings"}, inplace=True)
if "Directors" in myratings.columns:
    myratings["Director"] = myratings["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    myratings.drop(columns=["Directors"], inplace=True)

myratings = myratings[[c for c in desired_cols if c in myratings.columns]]
myratings = myratings.drop_duplicates(subset=["Movie ID"])

# --- Display My Ratings ---
st.write("---")
st.write("### My Ratings")

min_my_rating = st.slider(
    "Show movies with rating at least:",
    0, 10, 7,
    key="my_slider"
)

filtered_myratings = myratings[
    myratings["Personal Ratings"] >= min_my_rating
].sort_values("Personal Ratings", ascending=False)

st.dataframe(
    filtered_myratings.drop(columns=["Genre"], errors="ignore"),
    width="stretch",
    height=400
)