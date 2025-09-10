import streamlit as st
import pandas as pd

# ============================ 
# --- Robust CSV Loader ---
# ============================
def load_csv(path):
    """Load CSV handling quoted fields properly."""
    return pd.read_csv(path, quotechar='"', skipinitialspace=True)

# ============================
# --- Load My Ratings & Other Ratings ---
# ============================
myratings = load_csv("myratings.csv")
others = load_csv("othersratings1.csv")

# --- Standardize column names ---
for df in [myratings, others]:
    df.columns = df.columns.str.strip()
    if "Const" in df.columns:
        df.rename(columns={"Const": "Movie ID"}, inplace=True)

    # Keep only first director
    if "Directors" in df.columns:
        df["Director"] = df["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
        df.drop(columns=["Directors"], inplace=True)

    # Keep only first genre
    if "Genres" in df.columns:
        df["Genres"] = df["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

# --- Merge tables on Movie ID if needed (optional) ---
# e.g., to get IMDb Rating aligned with your ratings
merged_df = myratings.merge(
    others[["Movie ID", "IMDb Rating"]],
    on="Movie ID",
    how="left"
)

# ============================
# --- Streamlit Display ---
# ============================
st.set_page_config(layout="wide")
st.title("🎬 IMDb Data Explorer")

# My Ratings Table
st.write("### My Ratings")
st.dataframe(myratings, width="stretch", height=400)

# Other Ratings Table
st.write("### Other Ratings (IMDb)")
st.dataframe(others, width="stretch", height=400)

# Merged Table (optional)
st.write("### Merged Table (with IMDb Ratings)")
st.dataframe(merged_df, width="stretch", height=400)

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

# Display Hybrid Recommendations
st.write("### 🎬 Hybrid Recommendations")
recs = hybrid_recommender(myratings, others, min_imdb=5, top_n=100)
st.dataframe(recs)
