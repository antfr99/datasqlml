import streamlit as st
import pandas as pd

# --- Load Files ---
myratings = pd.read_csv("myratings.csv")
others = pd.read_csv("othersratings1.csv")

# --- Standardize column names ---
myratings.columns = myratings.columns.str.strip()
others.columns = others.columns.str.strip()

# --- Rename "Const" to "Movie ID" ---
for df in [myratings, others]:
    df.rename(columns={"Const": "Movie ID"}, inplace=True)

# --- Clean Directors: keep only first director ---
for df in [myratings, others]:
    if "Directors" in df.columns:
        df["Director"] = df["Directors"].fillna("").apply(
            lambda x: x.split(",")[0].strip() if x else ""
        )
        df.drop(columns=["Directors"], inplace=True)

# --- Clean Genres: keep only first genre ---
for df in [myratings, others]:
    if "Genres" in df.columns:
        df["Genres"] = df["Genres"].fillna("").apply(
            lambda x: x.split(",")[0].strip() if x else ""
        )

# --- Reset index for both ---
myratings = myratings.reset_index(drop=True)
others = others.reset_index(drop=True)

# --- Streamlit Config ---
st.set_page_config(layout="wide")
st.title("🎬 IMDb Data Explorer")

# --- My Ratings Table ---
st.write("### My Ratings (all columns)")
st.dataframe(myratings, width="stretch", height=400)

# --- Others Ratings Table ---
st.write("### Others Ratings (all columns)")
st.dataframe(others, width="stretch", height=400)
