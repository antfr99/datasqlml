import streamlit as st
import pandas as pd

# --- Load .xlsx files ---
try:
    IMDB_Ratings = pd.read_excel("imdbratings.xlsx")
    Personal_Ratings = pd.read_excel("myratings.xlsx")
except Exception as e:
    st.error(f"Error loading Excel files: {e}")
    IMDB_Ratings = pd.DataFrame()
    Personal_Ratings = pd.DataFrame()

# --- Remove empty/unnamed columns ---
def clean_unnamed_columns(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

IMDB_Ratings = clean_unnamed_columns(IMDB_Ratings)
Personal_Ratings = clean_unnamed_columns(Personal_Ratings)

# --- Streamlit Page ---
st.set_page_config(layout="wide")
st.title("IMDb & Personal Ratings - Cleaned Raw Tables")

# --- Show IMDb Ratings ---
st.write("---")
st.write("### IMDb Ratings Table")
if not IMDB_Ratings.empty:
    st.write("Columns:", IMDB_Ratings.columns.tolist())
    st.dataframe(IMDB_Ratings, width="stretch", height=400)
else:
    st.warning("IMDb Ratings Excel file is empty or failed to load.")

# --- Show Personal Ratings ---
st.write("---")
st.write("### Personal Ratings Table")
if not Personal_Ratings.empty:
    st.write("Columns:", Personal_Ratings.columns.tolist())
    st.dataframe(Personal_Ratings, width="stretch", height=400)
else:
    st.warning("Personal Ratings Excel file is empty or failed to load.")
