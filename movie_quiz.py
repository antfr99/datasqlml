import streamlit as st
import pandas as pd
import random

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Load Movies CSV ---
movies_df = pd.read_csv("movies.csv")
movies_df.columns = movies_df.columns.str.strip()

# Parse dates for proper sorting where needed
if "Date Rated" in movies_df.columns:
    movies_df["Date Rated"] = pd.to_datetime(movies_df["Date Rated"], errors="coerce")
if "Release Date" in movies_df.columns:
    movies_df["Release Date"] = pd.to_datetime(movies_df["Release Date"], errors="coerce")

# --- Intro ---
st.title("SQL Movie Quiz 🎬")
st.write(
    "This is a small personal project that combines **AI, Python, SQL, IMDb data, GitHub, and Streamlit**. "
    "Answer SQL-style questions (only using the exported IMDb fields) and explore the real movie data below."
)

st.write("---")

# Helper: build and persist shuffled options for each question so the order doesn't change on reruns
def get_shuffled_options(qkey: str, correct: str, distractors: list[str]) -> list[str]:
    opts_key = f"{qkey}_opts"
    if opts_key not in st.session_state:
        choices = distractors + [correct]
        random.shuffle(choices)
        st.session_state[opts_key] = choices
    return ["-- Select an option --"] + st.session_state[opts_key]

# Helper: render a radio question (label must be non-empty for accessibility)
def render_question(qnum: int, qkey: str, qtext: str, correct: str, distractors: list[str], df_display=None):
    label = f"Q{qnum}. {qtext}"
    options = get_shuffled_options(qkey, correct, distractors)
    selection = st.radio(label, options, key=qkey)  # non-empty label avoids Streamlit warning
    if selection == correct:
        st.success("✅ Correct!")
        if df_display is not None:
            st.dataframe(df_display, width="stretch", height=320)
    elif selection != "-- Select an option --":
        st.error("❌ Try again.")
    # return the chosen value (we'll compute score later)
    return selection

# Build question definitions (only IMDb Rating used; no 'Your Rating')
easy_questions = [
    {
        "key": "q1",
        "text": "Retrieve all movies from the dataset.",
        "correct": "SELECT * FROM movies",
        "distractors": ["SELECT Title, [IMDb Rating] FROM movies", "DELETE FROM movies"],
        "df": movies_df
    },
    {
        "key": "q2",
        "text": "Retrieve the Title and IMDb Rating for all movies.",
        "correct": "SELECT Title, [IMDb Rating] FROM movies",
        "distractors": ["SELECT COUNT(*) FROM movies", "SELECT * FROM movies WHERE [IMDb Rating] > 9"],
        "df": movies_df[["Title", "IMDb Rating"]]
    },
    {
        "key": "q3",
        "text": "Find all movies where IMDb Rating is greater than or equal to 9.",
        "correct": "SELECT * FROM movies WHERE [IMDb Rating] >= 9",
        "distractors": ["SELECT * FROM movies WHERE [IMDb Rating] > 9", "SELECT Title FROM movies"],
        "df": movies_df[movies_df["IMDb Rating"] >= 9].sort_values("IMDb Rating", ascending=False)
    },
    {
        "key": "q4",
        "text": "Count the total number of movies in the dataset.",
        "correct": "SELECT COUNT(*) FROM movies",
        "distractors": ["SELECT AVG([IMDb Rating]) FROM movies", "SELECT Title FROM movies"],
        "df": None
    },
    {
        "key": "q5",
        "text": "Find all unique Title Types in the dataset.",
        "correct": "SELECT DISTINCT [Title Type] FROM movies",
        "distractors": ["SELECT * FROM movies", "SELECT Title FROM movies WHERE [Title Type] = 'movie'"],
        "df": None
    }
]

intermediate_questions = [
    {
        "key": "q6",
        "text": "Find all movies released after the year 2015.",
        "correct": "SELECT * FROM movies WHERE Year > 2015",
        "distractors": ["SELECT * FROM movies WHERE [IMDb Rating] > 2015", "SELECT Year FROM movies"],
        "df": movies_df[movies_df["Year"] > 2015] if "Year" in movies_df.columns else None
    },
    {
        "key": "q7",
        "text": "List all movies sorted by IMDb Rating in descending order.",
        "correct": "SELECT * FROM movies ORDER BY [IMDb Rating] DESC",
        "distractors": ["SELECT * FROM movies ORDER BY [Num Votes] DESC", "SELECT * FROM movies ORDER BY Title ASC"],
        "df": movies_df.sort_values("IMDb Rating", ascending=False)
    },
    {
        "key": "q8",
        "text": "Find the average IMDb Rating of all movies.",
        "correct": "SELECT AVG([IMDb Rating]) FROM movies",
        "distractors": ["SELECT AVG([IMDb Rating]) FROM movies WHERE Title LIKE '%The%'", "SELECT COUNT(*) FROM movies"],
        "df": None
    },
    {
        "key": "q9",
        "text": "Group movies by Genres and count how many there are in each genre.",
        "correct": "SELECT Genres, COUNT(*) FROM movies GROUP BY Genres",
        "distractors": ["SELECT COUNT(Genres) FROM movies", "SELECT DISTINCT Genres FROM movies"],
        "df": movies_df.groupby("Genres").size().reset_index(name="Count")
    },
    {
        "key": "q10",
        "text": "Find the highest-rated movie (IMDb Rating).",
        "correct": "SELECT Title, [IMDb Rating] FROM movies ORDER BY [IMDb Rating] DESC LIMIT 1",
        "distractors": ["SELECT MAX([IMDb Rating]) FROM movies", "SELECT Title FROM movies WHERE [IMDb Rating] = 10"],
        "df": movies_df.sort_values("IMDb Rating", ascending=False).head(1)[["Title", "IMDb Rating"]]
    },
    {
        "key": "q11",
        "text": "Find all movies directed by Christopher Nolan.",
        "correct": "SELECT * FROM movies WHERE Directors = 'Christopher Nolan'",
        "distractors": ["SELECT * FROM movies WHERE Title = 'Christopher Nolan'", "SELECT * FROM movies"],
        "df": movies_df[movies_df["Directors"] == "Christopher Nolan"] if "Directors" in movies_df.columns else None
    },
    {
        "key": "q12",
        "text": "Calculate the average IMDb Rating for each Year.",
        "correct": "SELECT Year, AVG([IMDb Rating]) FROM movies GROUP BY Year",
        "distractors": ["SELECT Year, COUNT(*) FROM movies GROUP BY Year", "SELECT DISTINCT Year FROM movies"],
        "df": movies_df.groupby("Year")["IMDb Rating"].mean().reset_index() if "Year" in movies_df.columns else None
    },
    {
        "key": "q13",
        "text": "Find the top 5 movies with the most Num Votes.",
        "correct": "SELECT * FROM movies ORDER BY [Num Votes] DESC LIMIT 5",
        "distractors": ["SELECT MAX([Num Votes]) FROM movies", "SELECT COUNT(*) FROM movies"],
        "df": movies_df.sort_values("Num Votes", ascending=False).head(5) if "Num Votes" in movies_df.columns else None
    },
    {
        "key": "q14",
        "text": "Retrieve movies where IMDb Rating is greater than 8.5.",
        "correct": "SELECT * FROM movies WHERE [IMDb Rating] > 8.5",
        "distractors": ["SELECT * FROM movies WHERE [IMDb Rating] < 8.5", "SELECT Title FROM movies WHERE [IMDb Rating] > 8.5"],
        "df": movies_df[movies_df["IMDb Rating"] > 8.5].sort_values("IMDb Rating", ascending=False)
    },
    {
        "key": "q15",
        "text": "Find the longest movie (Runtime in minutes).",
        "correct": "SELECT Title, [Runtime (mins)] FROM movies ORDER BY [Runtime (mins)] DESC LIMIT 1",
        "distractors": ["SELECT MAX([Runtime (mins)]) FROM movies", "SELECT Title FROM movies WHERE [Runtime (mins)] = 90"],
        "df": movies_df.sort_values("Runtime (mins)", ascending=False).head(1)[["Title", "Runtime (mins)"]] if "Runtime (mins)" in movies_df.columns else None
    }
]

difficult_questions = [
    {
        "key": "q16",
        "text": "Find the movie with the second-highest IMDb Rating using DENSE_RANK().",
        "correct": "SELECT Title, [IMDb Rating] FROM (SELECT Title, [IMDb Rating], DENSE_RANK() OVER (ORDER BY [IMDb Rating] DESC) AS rnk FROM movies) t WHERE rnk = 2",
        "distractors": ["SELECT Title, MAX([IMDb Rating]) FROM movies", "SELECT * FROM movies WHERE [IMDb Rating] = 2"],
        "df": movies_df.assign(Rank=movies_df["IMDb Rating"].rank(method="dense", ascending=False)).query("Rank == 2")[["Title", "IMDb Rating"]]
    },
    {
        "key": "q17",
        "text": "Use a CTE to find the top IMDb-rated movie per director.",
        "correct": "WITH cte AS (SELECT Directors, Title, [IMDb Rating], ROW_NUMBER() OVER (PARTITION BY Directors ORDER BY [IMDb Rating] DESC) AS rn FROM movies) SELECT * FROM cte WHERE rn = 1",
        "distractors": ["SELECT Directors, MAX([IMDb Rating]) FROM movies GROUP BY Directors", "SELECT DISTINCT Directors FROM movies"],
        "df": movies_df.sort_values(["Directors", "IMDb Rating"], ascending=[True, False]).groupby("Directors").head(1)[["Directors", "Title", "IMDb Rating"]] if "Directors" in movies_df.columns else None
    },
    {
        "key": "q18",
        "text": "Calculate a running total of Num Votes ordered by Release Date.",
        "correct": "SELECT [Release Date], [Num Votes], SUM([Num Votes]) OVER (ORDER BY [Release Date]) AS RunningTotal FROM movies",
        "distractors": ["SELECT SUM([Num Votes]) FROM movies", "SELECT * FROM movies ORDER BY [Num Votes]"],
        "df": (movies_df.sort_values("Release Date")[["Release Date", "Num Votes"]].assign(**{"Running Total": movies_df.sort_values("Release Date")["Num Votes"].cumsum()})) if "Num Votes" in movies_df.columns and "Release Date" in movies_df.columns else None
    },
    {
        "key": "q19",
        "text": "Find directors who have movies in the most unique Genres.",
        "correct": "SELECT Directors, COUNT(DISTINCT Genres) AS GenreCount FROM movies GROUP BY Directors ORDER BY GenreCount DESC",
        "distractors": ["SELECT Directors, COUNT(*) FROM movies GROUP BY Directors", "SELECT DISTINCT Genres FROM movies"],
        "df": movies_df.groupby("Directors")["Genres"].nunique().reset_index(name="Unique Genres").sort_values("Unique Genres", ascending=False) if "Directors" in movies_df.columns else None
    },
    {
        "key": "q20",
        "text": "Compare the IMDb Rating of each movie with the one rated just before it (LAG).",
        "correct": "SELECT Title, [IMDb Rating], LAG([IMDb Rating]) OVER (ORDER BY [Date Rated]) AS PrevIMDb FROM movies",
        "distractors": ["SELECT Title, [IMDb Rating] FROM movies ORDER BY [Date Rated]", "SELECT * FROM movies WHERE [IMDb Rating] > 5"],
        "df": movies_df.sort_values("Date Rated").assign(PrevIMDb=movies_df.sort_values("Date Rated")["IMDb Rating"].shift(1))[["Date Rated", "Title", "IMDb Rating", "PrevIMDb"]] if "Date Rated" in movies_df.columns else None
    },
    {
        "key": "q21",
        "text": "Perform a self-join to find movies with the same director rated on the same Date Rated.",
        "correct": "SELECT a.Title, b.Title, a.Directors, a.[Date Rated] FROM movies a JOIN movies b ON a.Directors = b.Directors AND a.[Date Rated] = b.[Date Rated] AND a.Const <> b.Const",
        "distractors": ["SELECT * FROM movies WHERE Directors IS NOT NULL", "SELECT DISTINCT Directors FROM movies"],
        "df": (lambda df=movies_df: df.merge(df, on=["Directors", "Date Rated"], suffixes=("_a", "_b")).query("Const_a != Const_b")[["Title_a", "Title_b", "Directors", "Date Rated"]] if {"Directors", "Date Rated", "Const"}.issubset(df.columns) else None)()
    },
    {
        "key": "q22",
        "text": "Find years between the earliest and latest Release Date where you didn’t rate any movie.",
        "correct": "SELECT y.Year FROM (SELECT MIN([Release Date]) AS MinYear, MAX([Release Date]) AS MaxYear FROM movies) r CROSS JOIN Years y WHERE y.Year BETWEEN r.MinYear AND r.MaxYear AND y.Year NOT IN (SELECT DISTINCT Year FROM movies)",
        "distractors": ["SELECT DISTINCT Year FROM movies", "SELECT * FROM movies ORDER BY [Release Date]"],
        "df": (lambda: (
            lambda ry: list(range(ry.min(), ry.max() + 1)) if not ry.empty else []
        )(pd.to_datetime(movies_df["Release Date"], errors="coerce").dt.year.dropna().astype(int)) )()
    },
    {
        "key": "q23",
        "text": "Find genres where the average IMDb Rating is below the overall average IMDb Rating.",
        "correct": "SELECT Genres FROM movies GROUP BY Genres HAVING AVG([IMDb Rating]) < (SELECT AVG([IMDb Rating]) FROM movies)",
        "distractors": ["SELECT AVG([IMDb Rating]) FROM movies", "SELECT DISTINCT Genres FROM movies"],
        "df": (lambda: (lambda overall: movies_df.groupby("Genres")["IMDb Rating"].mean().reset_index().query("`IMDb Rating` < @overall"))(movies_df["IMDb Rating"].mean()))()
    },
    {
        "key": "q24",
        "text": "Find the IMDb Rating value that appears most frequently.",
        "correct": "SELECT [IMDb Rating], COUNT(*) AS cnt FROM movies GROUP BY [IMDb Rating] ORDER BY cnt DESC LIMIT 1",
        "distractors": ["SELECT MAX([IMDb Rating]) FROM movies", "SELECT DISTINCT [IMDb Rating] FROM movies"],
        "df": (lambda: (pd.DataFrame({"MostCommon": [movies_df["IMDb Rating"].mode().iloc[0]]}) if not movies_df["IMDb Rating"].mode().empty else None))()
    },
    {
        "key": "q25",
        "text": "Find the average IMDb Rating per Year and the year-over-year difference.",
        "correct": "SELECT Year, AVG([IMDb Rating]) AS AvgIMDb, AVG([IMDb Rating]) - LAG(AVG([IMDb Rating])) OVER (ORDER BY Year) AS YoYDiff FROM movies GROUP BY Year ORDER BY Year",
        "distractors": ["SELECT Year, AVG([IMDb Rating]) FROM movies GROUP BY Year", "SELECT AVG([IMDb Rating]) FROM movies"],
        "df": (lambda: (lambda g: (g.assign(YoYDiff=g["IMDb Rating"].diff()).rename(columns={"IMDb Rating": "AvgIMDb"}) if g is not None else None)(movies_df.groupby("Year")["IMDb Rating"].mean().reset_index()) ))()
    }
]

# Render sections and questions
st.header("🟢 Easy SQL Questions")
qnum = 1
for q in easy_questions:
    render_question(qnum, q["key"], q["text"], q["correct"], q["distractors"], q["df"])
    qnum += 1

st.header("🟡 Intermediate SQL Questions")
for q in intermediate_questions:
    render_question(qnum, q["key"], q["text"], q["correct"], q["distractors"], q["df"])
    qnum += 1

st.header("🔴 Difficult SQL Questions")
for q in difficult_questions:
    render_question(qnum, q["key"], q["text"], q["correct"], q["distractors"], q["df"])
    qnum += 1

# Reset button: clear answers and reshuffle options
if st.button("🔄 Reset Quiz (clear answers & reshuffle)"):
    keys_to_remove = [q["key"] for q in (easy_questions + intermediate_questions + difficult_questions)]
    for k in keys_to_remove:
        if k in st.session_state:
            del st.session_state[k]
        opts_k = f"{k}_opts"
        if opts_k in st.session_state:
            del st.session_state[opts_k]
    st.experimental_rerun()

# Final score calculation (computed deterministically)
all_questions = easy_questions + intermediate_questions + difficult_questions
total = len(all_questions)
correct_count = 0
for q in all_questions:
    sel = st.session_state.get(q["key"], "-- Select an option --")
    if sel == q["correct"]:
        correct_count += 1

st.write("---")
st.subheader("🎯 Your Quiz Score")
st.write(f"You answered **{correct_count}** out of **{total}** questions correctly.")
pct = round((correct_count/total)*100, 1) if total else 0
st.metric("Score", f"{correct_count}/{total}", f"{pct}%")
