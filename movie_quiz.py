import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Project Description ---
st.title("IMDb Data Experiment 🎬")
st.write(
    """
This is a small personal film data project using **Python Packages ( Streamlit, Pandas , PandasQL ), SQL, IMDb, GitHub, ChatGPT and Streamlit** 
"""
)


# ============================
# --- Load & Combine Other Ratings (IMDb Ratings) ---
# ============================

others1 = pd.read_csv("othersratings1.csv")
others2 = pd.read_csv("othersratings2.csv")

# Standardize columns
for df in [others1, others2]:
    df.columns = df.columns.str.strip()
    df.rename(columns={"Const": "Movie ID"}, inplace=True)  # keep IMDb Rating as is
    if "Directors" in df.columns:
        df["Director"] = df["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
        df.drop(columns=["Directors"], inplace=True)

# Keep only desired columns
desired_cols_others = [
    "Movie ID", "IMDb Rating", "Title", "URL",
    "Title Type", "Runtime (mins)", "Year",
    "Release Date", "Director", "Num Votes", "Genres"
]

others_combined = pd.concat([others1, others2], ignore_index=True)
others_combined = others_combined[[c for c in desired_cols_others if c in others_combined.columns]]
others_combined = others_combined.drop_duplicates(subset=["Movie ID"])

# --- Filter out movies with Num Votes <= 10000 ---
others_combined = others_combined[others_combined["Num Votes"] > 50000]

# --- Clean Genre column (keep only first genre) ---
if "Genres" in others_combined.columns:
    others_combined["Genres"] = others_combined["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

# --- Display Combined Other Ratings ---
st.write("---")
st.write("### IMDB Ratings ")

min_other_rating = st.slider(
    "Show movies with IMDb rating at least:",
    0, 10, 7,
    key="other_slider"
)

filtered_others = others_combined[
    others_combined["IMDb Rating"] >= min_other_rating
].sort_values("IMDb Rating", ascending=False)

st.dataframe(
    filtered_others,  # keep Genre column visible
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

# Keep only desired columns
desired_cols_myratings = [
    "Movie ID", "Personal Ratings", "Date Rated", "Title", "URL",
    "Title Type", "Runtime (mins)", "Year",
    "Release Date", "Director", "Genres"
]
myratings = myratings[[c for c in desired_cols_myratings if c in myratings.columns]]
myratings = myratings.drop_duplicates(subset=["Movie ID"])

# --- Clean Genre column (keep only first genre) ---
if "Genres" in myratings.columns:
    myratings["Genres"] = myratings["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")

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
    filtered_myratings,  # keep Genres column visible
    width="stretch",
    height=400
)




# ============================
# --- Content-Based Recommender (Genres Similarity) ---
# ============================
# ============================
# ============================
# --- Hybrid Recommender (Director + Genre + IMDb Rating) ---
# ============================

# ============================
# --- Hybrid Recommender (Director + Genre + IMDb Rating) ---
# ============================

# ============================
# --- Hybrid Recommender (Director + Genre + IMDb Rating) ---
# ============================
# ============================
# --- Hybrid Recommender (Director + Genre + IMDb Rating) ---
# ============================

def hybrid_recommender(myratings, others_combined, min_imdb=6, top_n=10000):
    # Clean IDs
    myratings["Movie ID"] = myratings["Movie ID"].astype(str).str.strip()
    others_combined["Movie ID"] = others_combined["Movie ID"].astype(str).str.strip()

    # 1. Movies I rated highly
    liked_movies = myratings[myratings["Personal Ratings"] >= 6]

    # 2. Collect favorite directors and ALL genres
    fav_directors = set(liked_movies["Director"].dropna().unique())
    fav_genres = set(g for g_list in liked_movies["Genres"].dropna()
                        for g in g_list.split(","))

    # 3. Broader candidate filter
    candidates = others_combined[
        (others_combined["IMDb Rating"] >= min_imdb) &
        (others_combined["Num Votes"] > 5000)   # relaxed from 50k
    ]

    # 4. Genre bonus map
    genre_bonus_map = {
        "Crime": 0.1,
        "Biography": 0.1,
        "Animation": 0.1,
        "Comedy": 0.5,
        "Drama": 0.5
    }

    def score_movie(row):
        director_bonus = 1.0 if row["Director"] in fav_directors else 0.0
        # handle multiple genres
        genres = [g.strip() for g in row["Genres"].split(",") if g]
        genre_bonus = max(
            (genre_bonus_map.get(g, 0.2) if g in fav_genres else 0.2)
            for g in genres
        ) if genres else 0.2

        hybrid_score = row["IMDb Rating"] + director_bonus + genre_bonus
        return pd.Series({
            "Director Bonus": director_bonus,
            "Genre Bonus": genre_bonus,
            "Hybrid Score": hybrid_score
        })

    candidates = candidates.copy()
    bonuses = candidates.apply(score_movie, axis=1)
    candidates = pd.concat([candidates, bonuses], axis=1)

    # 5. Drop movies I already rated
    candidates = candidates[~candidates["Movie ID"].isin(myratings["Movie ID"])]

    # 6. Return sorted list
    return candidates.sort_values("Hybrid Score", ascending=False).head(top_n)[
        ["Title", "Director", "Genres", "IMDb Rating",
         "Director Bonus", "Genre Bonus", "Hybrid Score"]
    ]
