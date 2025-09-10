import pandas as pd
import csv
import streamlit as st

# --- Load CSV with quote handling ---
def load_quoted_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        # Sniff the delimiter
        sample = f.read(1024)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample)
        f.seek(0)
        reader = csv.reader(f, dialect)
        rows = list(reader)
    
    # Some rows may still be single string; split manually
    clean_rows = []
    for r in rows:
        if len(r) == 1:
            # Remove outer quotes and split on comma
            r = r[0].strip('"').replace('""', '"').split(',')
        clean_rows.append(r)

    # Create DataFrame
    df = pd.DataFrame(clean_rows[1:], columns=clean_rows[0])
    return df

# --- Load Files ---
myratings = load_quoted_csv("myratings.csv")
others = load_quoted_csv("othersratings1.csv")

# --- Clean Columns (first director/genre etc.) ---
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
