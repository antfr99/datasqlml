import streamlit as st
import pandas as pd

# --- Load with delimiter detection ---
def load_csv(path):
    try:
        # First try standard CSV (comma)
        return pd.read_csv(path)
    except Exception:
        # If fails, try semicolon
        return pd.read_csv(path, delimiter=";")

# --- Load Files ---
myratings = load_csv("myratings.csv")
others = load_csv("othersratings1.csv")

# --- Standardize column names ---
for df in [myratings, others]:
    df.columns = df.columns.str.strip()
    df.rename(columns={"Const": "Movie ID"}, inplace=True)

    # Clean Directors: only first director
    if "Directors" in df.columns:
        df["Director"] = df["Directors"].fillna("").apply(
            lambda x: x.split(",")[0].strip() if x else ""
        )
        df.drop(columns=["Directors"], inplace=True)

    # Clean Genres: only first genre
    if "Genres" in df.columns:
        df["Genres"] = df["Genres"].fillna("").apply(
            lambda x: x.split(",")[0].strip() if x else ""
        )

# --- Streamlit Config ---
st.set_page_config(layout="wide")
st.title("🎬 IMDb Data Explorer")

# --- My Ratings Table ---
st.write("### My Ratings")
st.dataframe(myratings, width="stretch", height=400)

# --- Others Ratings Table ---
st.write("### Others Ratings")
st.dataframe(others, width="stretch", height=400)
