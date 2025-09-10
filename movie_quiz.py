import streamlit as st
import pandas as pd

# ============================
# --- Load CSV Robustly ---
# ============================
def load_csv(path):
    """Load CSV with quote handling and stripping spaces."""
    df = pd.read_csv(path, quotechar='"', skipinitialspace=True)

    # Remove duplicate columns if any
    if df.columns.duplicated().any():
        df = df.loc[:, ~df.columns.duplicated()]

    return df

# ============================
# --- Load My Ratings ---
# ============================
myratings = load_csv("myratings.csv")

# Standardize columns
myratings.columns = myratings.columns.str.strip()
myratings.rename(columns={"Const": "Movie ID", "Your Rating": "Personal Ratings"}, inplace=True)

# Keep only first director if exists
if "Directors" in myratings.columns:
    myratings["Director"] = myratings["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    myratings.drop(columns=["Directors"], inplace=True)

# Keep only first genre if exists
if "Genres" in myratings.columns:
    myratings["Genres"] = myratings["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

# Drop duplicate Movie IDs
myratings = myratings.drop_duplicates(subset=["Movie ID"])

# ============================
# --- Load Other Ratings ---
# ============================
others = load_csv("othersratings1.csv")

# Drop 'Position' column if exists
if "Position" in others.columns:
    others.drop(columns=["Position"], inplace=True)

# Standardize columns
others.columns = others.columns.str.strip()
others.rename(columns={"Const": "Movie ID"}, inplace=True)

# Keep only first director if exists
if "Directors" in others.columns:
    others["Director"] = others["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    others.drop(columns=["Directors"], inplace=True)

# Keep only first genre if exists
if "Genres" in others.columns:
    others["Genres"] = others["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

# Drop duplicate Movie IDs
others = others.drop_duplicates(subset=["Movie ID"])

# Ensure Movie ID is string in both
myratings["Movie ID"] = myratings["Movie ID"].astype(str)
others["Movie ID"] = others["Movie ID"].astype(str)

# ============================
# --- Streamlit Display ---
# ============================
st.set_page_config(layout="wide")
st.title("🎬 IMDb Data Explorer")

st.write("### My Ratings")
st.dataframe(myratings, width="stretch", height=400)

st.write("### Other Ratings (IMDb)")
st.dataframe(others, width="stretch", height=400)

# ============================
# --- Hybrid Recommender ---
# ============================
def hybrid_recommender(myratings, others, min_imdb=7, top_n=100):
    # 1. Highly rated movies
    liked_movies = myratings[myratings["Personal Ratings"] >= 7]
    if liked_movies.empty:
        st.warning("No highly-rated movies in your list.")
        return pd.DataFrame()

    # 2. Favorite directors and genres
    fav_directors = set(liked_movies["Director"].dropna().unique())
    fav_genres = set(liked_movies["Genres"].dropna().unique())

    # 3. Candidates from others
    candidates = others[others["IMDb Rating"] >= min_imdb].copy()

    # 4. Score function
    genre_bonus_map = {"Crime":0.1,"Biography":0.1,"Animation":0.1,
                       "Comedy":0.5,"Drama":0.5,"Romance":0.5,
                       "Adventure":0.2,"Horror":0.2,"Action":0.2}

    def score_movie(row):
        director_bonus = 1.0 if row["Director"] in fav_directors else 0.0
        if pd.isna(row["Genres"]) or row["Genres"] == "":
            genre_bonus = 0.2
        elif row["Genres"] in fav_genres:
            genre_bonus = genre_bonus_map.get(row["Genres"], 0.0)
        else:
            genre_bonus = 0.2
        hybrid_score = row["IMDb Rating"] + director_bonus + genre_bonus
        return pd.Series({"Director Bonus": director_bonus,
                          "Genre Bonus": genre_bonus,
                          "Hybrid Score": hybrid_score})

    bonuses = candidates.apply(score_movie, axis=1)
    candidates = pd.concat([candidates, bonuses], axis=1)

    # 5. Exclude already rated movies
    candidates = candidates[~candidates["Movie ID"].isin(myratings["Movie ID"])]

    # 6. Return top_n
    return candidates.sort_values("Hybrid Score", ascending=False).head(top_n)[
        ["Title","Director","Genres","IMDb Rating","Director Bonus","Genre Bonus","Hybrid Score"]
    ]

# ============================
# --- Display Hybrid Recommendations ---
# ============================
st.write("### 🎬 Hybrid Recommendations")
recs = hybrid_recommender(myratings, others, min_imdb=5, top_n=100)
st.dataframe(recs, width="stretch", height=400)
