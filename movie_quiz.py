import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(layout="wide")

# ============================
# --- Load My Ratings ---
# ============================
myratings = pd.read_csv("myratings.csv")
myratings.columns = myratings.columns.str.strip()
myratings.rename(columns={"Const": "Movie ID", "Your Rating": "Personal Ratings"}, inplace=True)

# Keep only first director if multiple
if "Directors" in myratings.columns:
    myratings["Director"] = myratings["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    myratings.drop(columns=["Directors"], inplace=True)

# Keep only first genre if multiple
if "Genres" in myratings.columns:
    myratings["Genres"] = myratings["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

# Convert Personal Ratings to numeric
myratings["Personal Ratings"] = pd.to_numeric(myratings["Personal Ratings"], errors="coerce")

# Drop duplicates
myratings = myratings.drop_duplicates(subset=["Movie ID"])

# ============================
# --- Load Others Ratings ---
# ============================
others = pd.read_csv("othersratings1.csv")
others.columns = others.columns.str.strip()
others.rename(columns={"Const": "Movie ID"}, inplace=True)

# Keep only first director if multiple
if "Directors" in others.columns:
    others["Director"] = others["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    others.drop(columns=["Directors"], inplace=True)

# Keep only first genre if multiple
if "Genres" in others.columns:
    others["Genres"] = others["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

# Convert numeric fields
others["IMDb Rating"] = pd.to_numeric(others["IMDb Rating"], errors="coerce")
others["Num Votes"] = pd.to_numeric(others["Num Votes"], errors="coerce")

# Drop duplicates
others = others.drop_duplicates(subset=["Movie ID"])

# ============================
# --- Hybrid Recommender ---
# ============================
def hybrid_recommender(myratings, others, min_imdb=6, top_n=1000):
    # 1. Get movies I rated highly
    liked_movies = myratings[myratings["Personal Ratings"] >= 6]
    if liked_movies.empty:
        st.warning("No highly-rated movies in your list.")
        return pd.DataFrame()

    # 2. Collect favorite directors and genres
    fav_directors = set(liked_movies["Director"].dropna().unique())
    fav_genres = set(liked_movies["Genres"].dropna().unique())

    # 3. Filter candidates
    candidates = others[
        (others["IMDb Rating"] >= min_imdb) &
        (others["Num Votes"] > 10000)
    ].copy()

    # 4. Genre bonus mapping
    genre_bonus_map = {
        "Crime": 0.1,
        "Biography": 0.1,
        "Animation": 0.1,
        "Comedy": 0.5,
        "Drama": 0.5,
        "Romance": 0.5,
        "Adventure": 0.2,
        "Horror": 0.2,
        "Action": 0.2
    }

    # 5. Score candidates
    def score_movie(row):
        director_bonus = 1.0 if row["Director"] in fav_directors else 0.0
        genre_bonus = genre_bonus_map.get(row["Genres"], 0.2) if row["Genres"] in fav_genres else 0.2
        hybrid_score = row["IMDb Rating"] + director_bonus + genre_bonus
        return pd.Series({
            "Director Bonus": director_bonus,
            "Genre Bonus": genre_bonus,
            "Hybrid Score": hybrid_score
        })

    bonuses = candidates.apply(score_movie, axis=1)
    candidates = pd.concat([candidates, bonuses], axis=1)

    # 6. Exclude movies already rated
    candidates = candidates[~candidates["Movie ID"].isin(myratings["Movie ID"])]

    # 7. Return top_n
    return candidates.sort_values("Hybrid Score", ascending=False).head(top_n)[
        ["Title", "Director", "Genres", "IMDb Rating", "Director Bonus", "Genre Bonus", "Hybrid Score"]
    ]

# ============================
# --- Streamlit Display ---
# ============================
st.write("### 🎬 Hybrid Recommendations")
recs = hybrid_recommender(myratings, others, min_imdb=6, top_n=1000)
st.dataframe(recs, width="stretch", height=600)
