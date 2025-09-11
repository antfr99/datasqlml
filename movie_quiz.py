import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb Data Experiment 🎬")
st.write("""
This is a small personal film data project using **Streamlit, Pandas, IMDb data**.
""")

# ============================
# --- Load CSVs Robustly ---
# ============================

def load_csv(file_path):
    """Load CSV handling quotes and commas inside fields."""
    return pd.read_csv(
        file_path,
        encoding="utf-8",
        quotechar='"',
        dtype=str,  # read all as string to avoid parsing errors
        on_bad_lines='skip'  # skip malformed lines
    )

# Load my ratings
myratings = load_csv("myratings.csv")

# Load other ratings (only othersratings1.csv for simplicity)
others = load_csv("othersratings1.csv")

# ============================
# --- Clean & Standardize Columns ---
# ============================

def clean_movies(df):
    df.columns = df.columns.str.strip()
    
    # Movie ID
    if "Const" in df.columns:
        df.rename(columns={"Const": "Movie ID"}, inplace=True)
    
    # Personal Ratings
    if "Your Rating" in df.columns:
        df.rename(columns={"Your Rating": "Personal Ratings"}, inplace=True)
    
    # Director: keep first if multiple
    if "Directors" in df.columns:
        df["Director"] = df["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
        df.drop(columns=["Directors"], inplace=True)
    
    # Genres: keep first if multiple
    if "Genres" in df.columns:
        df["Genres"] = df["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    
    # Convert numeric columns
    for col in ["IMDb Rating", "Personal Ratings", "Num Votes", "Runtime (mins)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

myratings = clean_movies(myratings)
others = clean_movies(others)

# Drop duplicates
myratings = myratings.drop_duplicates(subset=["Movie ID"])
others = others.drop_duplicates(subset=["Movie ID"])

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
# --- Display Other Ratings ---
# ============================

st.write("---")
st.write("### Other IMDb Ratings")
st.dataframe(
    others.sort_values("IMDb Rating", ascending=False),
    width="stretch",
    height=400
)

# ============================
# --- Hybrid Recommender ---
# ============================

def hybrid_recommender(myratings, others, min_imdb=6, top_n=1000):
    # Only consider movies I rated highly
    liked = myratings[myratings["Personal Ratings"] >= 6]
    if liked.empty:
        st.warning("No highly-rated movies in your list.")
        return pd.DataFrame()
    
    fav_directors = set(liked["Director"].dropna())
    fav_genres = set(liked["Genres"].dropna())
    
    # Filter candidates
    candidates = others[
        (others["IMDb Rating"] >= min_imdb) &
        (~others["Movie ID"].isin(myratings["Movie ID"]))  # exclude already rated
    ].copy()
    
    # Genre bonus mapping
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

# ============================
# --- Display Hybrid Recommendations ---
# ============================

st.write("---")
st.write("### 🎬 Hybrid Recommendations")
recs = hybrid_recommender(myratings, others, min_imdb=5, top_n=1000)
st.dataframe(recs)
