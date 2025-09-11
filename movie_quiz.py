# ============================
# --- Streamlit Hybrid Recommender App ---
# ============================
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ============================
# --- Load My Ratings ---
# ============================
myratings = pd.read_csv("myratings.csv")
myratings.columns = myratings.columns.str.strip()
myratings.rename(columns={"Const": "Movie ID", "Your Rating": "Personal Ratings"}, inplace=True)

if "Directors" in myratings.columns:
    myratings["Director"] = myratings["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    myratings.drop(columns=["Directors"], inplace=True)

desired_cols_myratings = [
    "Movie ID", "Personal Ratings", "Date Rated", "Title", "URL", "Title Type",
    "Runtime (mins)", "Year", "Release Date", "Director", "Genres"
]
myratings = myratings[[c for c in desired_cols_myratings if c in myratings.columns]]
myratings = myratings.drop_duplicates(subset=["Movie ID"])

if "Genres" in myratings.columns:
    myratings["Genres"] = myratings["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

st.write("### 🎞 My Ratings")
st.dataframe(myratings, width="stretch", height=300)

# ============================
# --- Load Others Ratings 1 ---
# ============================
others1 = pd.read_csv("othersratings1.csv")
others1.columns = others1.columns.str.strip()
others1.rename(columns={"Const": "Movie ID"}, inplace=True)

if "Directors" in others1.columns:
    others1["Director"] = others1["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    others1.drop(columns=["Directors"], inplace=True)

desired_cols_others = [
    "Movie ID", "IMDb Rating", "Title", "URL", "Title Type", "Runtime (mins)",
    "Year", "Release Date", "Director", "Num Votes", "Genres"
]
others1 = others1[[c for c in desired_cols_others if c in others1.columns]]
others1 = others1.drop_duplicates(subset=["Movie ID"])

if "Genres" in others1.columns:
    others1["Genres"] = others1["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

# Filter out low-vote movies
others1 = others1[others1["Num Votes"] > 10000]

st.write("### 🌍 IMDb Ratings (Others)")
st.dataframe(others1, width="stretch", height=300)

# ============================
# --- Hybrid Recommender ---
# ============================
def hybrid_recommender(myratings, others, min_imdb=7, top_n=100):
    liked_movies = myratings[myratings["Personal Ratings"] >= 7]
    if liked_movies.empty:
        st.warning("No highly-rated movies in your list.")
        return pd.DataFrame()

    fav_directors = set(liked_movies["Director"].dropna().unique())
    fav_genres = set(liked_movies["Genres"].dropna().unique())

    candidates = others[
        (others["IMDb Rating"] >= min_imdb) &
        (others["Num Votes"] > 10000)
    ]

    genre_bonus_map = {
        "Crime": 0.1, "Biography": 0.1, "Animation": 0.1,
        "Comedy": 0.5, "Drama": 0.5, "Romance": 0.5,
        "Adventure": 0.2, "Horror": 0.2, "Action": 0.2
    }

    def score_movie(row):
        director_bonus = 1.0 if row["Director"] in fav_directors else 0.0

        if pd.isna(row["Genres"]) or row["Genres"] == "":
            genre_bonus = 0.2
        elif row["Genres"] in fav_genres:
            genre_bonus = genre_bonus_map.get(row["Genres"], 0.0)
        else:
            genre_bonus = 0.2

        hybrid_score = row["IMDb Rating"] + director_bonus + genre_bonus
        return pd.Series({
            "Director Bonus": director_bonus,
            "Genre Bonus": genre_bonus,
            "Hybrid Score": hybrid_score
        })

    candidates = candidates.copy()
    bonuses = candidates.apply(score_movie, axis=1)
    candidates = pd.concat([candidates, bonuses], axis=1)

    candidates = candidates[~candidates["Movie ID"].isin(myratings["Movie ID"])]

    return candidates.sort_values("Hybrid Score", ascending=False).head(top_n)[
        ["Title", "Director", "Genres", "IMDb Rating", "Director Bonus", "Genre Bonus", "Hybrid Score"]
    ]

# ============================
# --- Show Code + Results ---
# ============================
with st.expander("📜 Show Hybrid Recommender Code"):
    st.code(hybrid_recommender, language="python")

st.write("### 🎬 Hybrid Recommendations")
recs = hybrid_recommender(myratings, others1, min_imdb=5, top_n=500)
st.dataframe(recs, width="stretch", height=500)
