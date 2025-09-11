import pandas as pd
import streamlit as st

# --- Robust CSV loader ---
def load_csv(file_path):
    """Load CSV handling quotes and commas inside fields robustly."""
    df = pd.read_csv(
        file_path,
        encoding="utf-8",
        quotechar='"',   # important to correctly parse fields with commas
        sep=',',
        dtype=str,
        on_bad_lines='skip',
        engine='python'  # safer for messy CSVs
    )
    return df

# --- Clean & Standardize ---
def clean_movies(df):
    df.columns = df.columns.str.strip()

    # Map columns
    df.rename(columns={
        "Const": "Movie ID",
        "Your Rating": "Personal Ratings",
        "Directors": "Director"
    }, inplace=True)

    # Take first director
    if "Director" in df.columns:
        df["Director"] = df["Director"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

    # Take first genre
    if "Genres" in df.columns:
        df["Genres"] = df["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

    # Convert numeric fields
    for col in ["IMDb Rating", "Personal Ratings", "Num Votes", "Runtime (mins)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

# --- Load CSVs ---
myratings = clean_movies(load_csv("myratings.csv"))
others = clean_movies(load_csv("othersratings1.csv"))

# Ensure expected columns exist
expected_cols = ["Movie ID","Title","Original Title","URL","Title Type",
                 "IMDb Rating","Runtime (mins)","Year","Genres","Num Votes",
                 "Release Date","Director","Personal Ratings","Date Rated"]
for col in expected_cols:
    if col not in others.columns:
        others[col] = None
others = others[expected_cols]

# ============================
# --- Display Other Ratings ---
# ============================
st.write("### IMDb Ratings")
st.dataframe(
    others.sort_values("IMDb Rating", ascending=False),
    width="stretch",
    height=400
)

# ============================
# --- Display My Ratings ---
# ============================
st.write("---")
st.write("### My Ratings")
st.dataframe(
    myratings.sort_values("Personal Ratings", ascending=False),
    width="stretch",
    height=400
)

# ============================
# --- Hybrid Recommendations ---
# ============================
def hybrid_recommender(myratings, others, min_imdb=6, top_n=1000):
    liked = myratings[myratings["Personal Ratings"] >= 6]
    if liked.empty:
        st.warning("No highly-rated movies in your list.")
        return pd.DataFrame()
    
    fav_directors = set(liked["Director"].dropna())
    fav_genres = set(liked["Genres"].dropna())
    
    candidates = others[
        (others["IMDb Rating"] >= min_imdb) &
        (~others["Movie ID"].isin(myratings["Movie ID"]))
    ].copy()
    
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
    
    def score(row):
        director_bonus = 1.0 if row["Director"] in fav_directors else 0.0
        genre_bonus = genre_bonus_map.get(row["Genres"], 0.2)
        return pd.Series({
            "Director Bonus": director_bonus,
            "Genre Bonus": genre_bonus,
            "Hybrid Score": row["IMDb Rating"] + director_bonus + genre_bonus
        })
    
    scores = candidates.apply(score, axis=1)
    candidates = pd.concat([candidates, scores], axis=1)
    
    return candidates.sort_values("Hybrid Score", ascending=False).head(top_n)[
        ["Title", "Director", "Genres", "IMDb Rating", "Director Bonus", "Genre Bonus", "Hybrid Score"]
    ]

st.write("---")
st.write("### 🎬 Hybrid Recommendations")
recs = hybrid_recommender(myratings, others, min_imdb=5, top_n=1000)
st.dataframe(recs)
