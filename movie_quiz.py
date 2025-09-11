import streamlit as st
import pandas as pd

# --- Load CSVs ---
try:
    IMDB_Ratings = pd.read_csv("imdbratings.csv", encoding='utf-8-sig')
    Personal_Ratings = pd.read_csv("myratings.csv", encoding='utf-8-sig')
except Exception as e:
    st.error(f"Error loading CSV files: {e}")
    IMDB_Ratings = pd.DataFrame()
    Personal_Ratings = pd.DataFrame()

# --- Streamlit Page ---
st.set_page_config(layout="wide")
st.title("IMDb & Personal Ratings - Raw Tables")

# --- Show IMDb Ratings ---
st.write("---")
st.write("### IMDb Ratings Table")
if not IMDB_Ratings.empty:
    st.write("Columns:", IMDB_Ratings.columns.tolist())
    st.dataframe(IMDB_Ratings, width="stretch", height=400)
else:
    st.warning("IMDb Ratings CSV is empty or failed to load.")

# --- Show Personal Ratings ---
st.write("---")
st.write("### Personal Ratings Table")
if not Personal_Ratings.empty:
    st.write("Columns:", Personal_Ratings.columns.tolist())
    st.dataframe(Personal_Ratings, width="stretch", height=400)
else:
    st.warning("Personal Ratings CSV is empty or failed to load.")
