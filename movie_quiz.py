import pandas as pd
import streamlit as st
import csv
from io import StringIO

# --- Robust CSV loader with column alignment ---
def load_csv_fix(file_path, expected_cols):
    """
    Load a CSV robustly, fix rows with misaligned columns, and return a clean DataFrame.
    """
    clean_rows = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, quotechar='"', delimiter=',', skipinitialspace=True)
        header = next(reader)
        header = [h.strip() for h in header]
        
        for row in reader:
            # If row too short, pad with empty strings
            if len(row) < len(expected_cols):
                row += [""] * (len(expected_cols) - len(row))
            # If row too long, merge extra columns into the last field
            elif len(row) > len(expected_cols):
                row = row[:len(expected_cols)-1] + [",".join(row[len(expected_cols)-1:])]
            clean_rows.append(row)
    
    # Convert to DataFrame
    df = pd.DataFrame(clean_rows, columns=expected_cols, dtype=str)
    
    # Strip whitespace
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Convert numeric columns
    for col in ["IMDb Rating", "Personal Ratings", "Num Votes", "Runtime (mins)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # First director
    if "Director" in df.columns:
        df["Director"] = df["Director"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    
    # First genre
    if "Genres" in df.columns:
        df["Genres"] = df["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    
    return df

# --- Expected columns ---
expected_cols = ["Position","Movie ID","Created","Modified","Description",
                 "Title","Original Title","URL","Title Type","IMDb Rating",
                 "Runtime (mins)","Year","Genres","Num Votes","Release Date",
                 "Director","Personal Ratings","Date Rated"]

# --- Load CSV ---
others = load_csv_fix("othersratings1.csv", expected_cols)

st.write("### IMDb Ratings (Cleaned)")
st.dataframe(others.sort_values("IMDb Rating", ascending=False))

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
