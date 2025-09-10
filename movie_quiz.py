import pandas as pd
import csv
import streamlit as st

def load_csv_proper(path):
    with open(path, newline='', encoding='utf-8') as f:
        # Use csv.reader with correct quotechar
        reader = csv.reader(f, delimiter=',', quotechar='"')
        rows = list(reader)

    # First row is header
    header = rows[0]
    data = rows[1:]

    # Make DataFrame
    df = pd.DataFrame(data, columns=header)
    return df

# --- Load Files ---
myratings = load_csv_proper("myratings.csv")
others = load_csv_proper("othersratings1.csv")

# --- Clean Columns ---
def clean_df(df):
    df.columns = df.columns.str.strip()
    if "Const" in df.columns:
        df.rename(columns={"Const": "Movie ID"}, inplace=True)

    if "Directors" in df.columns:
        df["Director"] = df["Directors"].fillna("").apply(lambda x: x.split(",")[0].strip() if x else "")
        df.drop(columns=["Directors"], inplace=True)

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
