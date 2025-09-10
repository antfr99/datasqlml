import pandas as pd
import streamlit as st

# --- Robust CSV loader ---
def load_csv(path):
    try:
        df = pd.read_csv(path, sep=None, engine="python", quotechar='"')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Failed to load {path}: {e}")
        return pd.DataFrame()

# --- Load Files ---
myratings = load_csv("myratings.csv")
others = load_csv("othersratings1.csv")

# --- Standardize column names and clean data ---
def clean_df(df):
    # Rename column
    if "Const" in df.columns:
        df.rename(columns={"Const": "Movie ID"}, inplace=True)
    
    # Keep only first director
    if "Directors" in df.columns:
        df["Director"] = df["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
        df.drop(columns=["Directors"], inplace=True)

    # Keep only first genre
    if "Genres" in df.columns:
        df["Genres"] = df["Genres"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
    
    return df

myratings = clean_df(myratings)
others = clean_df(others)

# --- Streamlit Display ---
st.set_page_config(layout="wide")
st.title("🎬 IMDb Data Explorer")

st.write("### My Ratings")
st.dataframe(myratings, width="stretch", height=400)

st.write("### Others Ratings")
st.dataframe(others, width="stretch", height=400)
