import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb/SQL/Machine Learning Python Data Project 🎬")
st.write("""
This is a small IMDb data project combining Python Packages (Pandas, PandasQL, Streamlit), SQL, and GitHub.
""")

# --- Load Excel files ---
try:
    IMDB_Ratings = pd.read_excel("imdbratings.xlsx")
    My_Ratings = pd.read_excel("myratings.xlsx")
    Votes = pd.read_excel("votes.xlsx")  # Optional votes source
except Exception as e:
    st.error(f"Error loading Excel files: {e}")
    IMDB_Ratings = pd.DataFrame()
    My_Ratings = pd.DataFrame()
    Votes = pd.DataFrame()

# --- Clean unnamed columns ---
def clean_unnamed_columns(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

IMDB_Ratings = clean_unnamed_columns(IMDB_Ratings)
My_Ratings = clean_unnamed_columns(My_Ratings)
Votes = clean_unnamed_columns(Votes)

# --- Merge votes ---
if not Votes.empty:
    IMDB_Ratings = IMDB_Ratings.merge(Votes, on="Movie ID", how="left")

# --- Show Tables ---
st.write("---")
st.write("### IMDb Ratings Table")
if not IMDB_Ratings.empty:
    st.dataframe(IMDB_Ratings, width="stretch", height=400)
else:
    st.warning("IMDb Ratings table is empty or failed to load.")

st.write("---")
st.write("### My Ratings Table")
if not My_Ratings.empty:
    st.dataframe(My_Ratings, width="stretch", height=400)
else:
    st.warning("My Ratings table is empty or failed to load.")

# --- Scenarios ---
scenario = st.radio(
    "Choose a scenario:",
    [
        "Scenario 1- SQL  ", 
        "Scenario 2- SQL", 
        "Scenario 3- SQL", 
        "Scenario 4-Python Machine Learning",
        "Scenario 5- Statistical Insights by Genre (Agreement %)"
    ]
)

# --- Scenario 1: SQL Playground ---
if scenario == "Scenario 1- SQL  ":
    st.markdown('<h3 style="color:green;">Scenario 1 (My Ratings vs IMDb):</h3>', unsafe_allow_html=True)
    st.write("Movies where my rating is different from the IMDb rating (more than 2 points).")
    
    default_query_1 = """SELECT 
       pr.Title,
       pr.[Your Rating],
       ir.[IMDb Rating],
       ABS(CAST(pr.[Your Rating] AS FLOAT) - CAST(ir.[IMDb Rating] AS FLOAT)) AS Rating_Diff,
       CASE 
            WHEN pr.[Your Rating] > ir.[IMDb Rating] THEN 'I Liked More'
            ELSE 'I Liked Less'
       END AS Disagreement_Type
FROM My_Ratings pr
JOIN IMDB_Ratings ir
    ON pr.[Movie ID] = ir.[Movie ID]
WHERE ABS(CAST(pr.[Your Rating] AS FLOAT) - CAST(ir.[IMDb Rating] AS FLOAT)) > 2
ORDER BY Rating_Diff DESC, ir.[Num Votes] DESC
LIMIT 1000;"""
    
    user_query = st.text_area("Enter SQL query:", default_query_1, height=500, key="sql1")
    if st.button("Run SQL Query", key="run_sql1"):
        try:
            result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
            st.dataframe(result, width="stretch", height=800)
        except Exception as e:
            st.error(f"Error in SQL query: {e}")

# --- Scenario 2: SQL Playground ---
if scenario == "Scenario 2- SQL":
    st.markdown('<h3 style="color:green;">Scenario 2 (Hybrid Recommendation):</h3>', unsafe_allow_html=True)
    st.write("""
    Recommend movies I haven't seen yet with a bonus point system:  
    - Director I liked before → +1 point  
    - Genre is Comedy or Drama → +0.5  
    - Other genres → +0.2
    """)
    
    default_query_2 = """SELECT ir.Title,
       ir.[IMDb Rating],
       ir.Director,
       ir.Genre,
       ir.Year,
       CASE WHEN ir.Director IN (SELECT DISTINCT Director FROM My_Ratings WHERE [Your Rating] >= 7) THEN 1 ELSE 0 END AS Director_Bonus,
       CASE WHEN ir.Genre IN ('Comedy','Drama') THEN 0.5 ELSE 0.2 END AS Genre_Bonus,
       ir.[IMDb Rating] 
       + CASE WHEN ir.Director IN (SELECT DISTINCT Director FROM My_Ratings WHERE [Your Rating] >= 7) THEN 1 ELSE 0 END
       + CASE WHEN ir.Genre IN ('Comedy','Drama') THEN 0.5 ELSE 0.2 END AS Recommendation_Score
FROM IMDB_Ratings ir
LEFT JOIN My_Ratings pr
    ON ir.[Movie ID] = pr.[Movie ID]
WHERE pr.[Your Rating] IS NULL
  AND ir.[Num Votes] > 40000
ORDER BY Recommendation_Score DESC
LIMIT 10000;"""
    
    user_query = st.text_area("Enter SQL query:", default_query_2, height=500, key="sql2")
    if st.button("Run SQL Query", key="run_sql2"):
        try:
            result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
            st.dataframe(result, width="stretch", height=800)
        except Exception as e:
            st.error(f"Error in SQL query: {e}")

# --- Scenario 3: SQL Playground ---
if scenario == "Scenario 3- SQL":
    st.markdown('<h3 style="color:green;">Scenario 3 (Decade Discovery – Top Unseen Films by Decade):</h3>', unsafe_allow_html=True)
    st.write("""
    Shows highest-rated unseen films grouped by decade.  
    Removes duplicates and limits results to the top 20 per decade.
    """)
    
    default_query_3 = """
WITH Deduped AS (
    SELECT DISTINCT ir.[Movie ID], 
           ir.Title,
           ir.[IMDb Rating],
           ir.[Num Votes],
           ir.Genre,
           ir.Director,
           ir.Year,
           (ir.Year / 10) * 10 AS Decade
    FROM IMDB_Ratings ir
)
SELECT *
FROM (
    SELECT d.*,
           ROW_NUMBER() OVER (PARTITION BY d.Decade ORDER BY d.[IMDb Rating] DESC, d.[Num Votes] DESC) AS RankInDecade
    FROM Deduped d
    LEFT JOIN My_Ratings pr
        ON d.[Movie ID] = pr.[Movie ID]
    WHERE pr.[Your Rating] IS NULL
      AND d.[Num Votes] > 50000
) ranked
WHERE RankInDecade <= 20
ORDER BY Decade, [IMDb Rating] DESC, [Num Votes] DESC;
"""
    
    user_query = st.text_area("Enter SQL query:", default_query_3, height=600, key="sql3")
    if st.button("Run SQL Query", key="run_sql3"):
        try:
            result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
            st.dataframe(result, width="stretch", height=800)
        except Exception as e:
            st.error(f"Error in SQL query: {e}")

# --- Scenario 4: Python ML ---
if scenario == "Scenario 4-Python Machine Learning":
    st.markdown('<h3 style="color:green;">Scenario 4 (Predict My Ratings – ML):</h3>', unsafe_allow_html=True)
    st.write("""
    Predict my ratings for unseen movies using a machine learning model.

    **How it works:**
    1. The model uses my existing ratings (`My_Ratings`) as training data.
    2. Features used include:  
       - IMDb Rating  
       - Genre  
       - Director  
       - Year of release  
       - Number of votes
    3. A Random Forest Regressor learns patterns from the movies I've already rated.
    4. The model predicts how I might rate movies I haven't seen yet (`Predicted Rating`).

    **Note:** Running the prediction may take over a 1 minute. Please be patient.
    """)
    
    ml_code = '''
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Merge IMDb and My Ratings
df_ml = IMDB_Ratings.merge(My_Ratings[['Movie ID','Your Rating']], on='Movie ID', how='left')
train_df = df_ml[df_ml['Your Rating'].notna()]
predict_df = df_ml[df_ml['Your Rating'].isna()]

# Features
categorical_features = ['Genre', 'Director']
numerical_features = ['IMDb Rating', 'Num Votes', 'Year']

# Preprocessing + Model
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numerical_features)
    ]
)

model = Pipeline([
    ('prep', preprocessor),
    ('reg', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train & predict
X_train = train_df[categorical_features + numerical_features]
y_train = train_df['Your Rating']
model.fit(X_train, y_train)
X_pred = predict_df[categorical_features + numerical_features]
predict_df['Predicted Rating'] = model.predict(X_pred)
predict_df
'''

    user_ml_code = st.text_area("Python ML Code (editable)", ml_code, height=1000)

    st.sidebar.header("ML Options")
    min_votes = st.sidebar.slider("Minimum IMDb Votes", 0, 500000, 50000, step=5000)
    top_n = st.sidebar.slider("Number of Top Predictions", 5, 50, 30, step=5)

    if st.button("Run Python ML Code", key="run_ml"):
        try:
            local_vars = {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings}
            exec(user_ml_code, {}, local_vars)
            predict_df = local_vars['predict_df']
            predict_df = predict_df[predict_df['Num Votes'] >= min_votes]
            st.dataframe(
                predict_df[['Title','IMDb Rating','Genre','Director','Predicted Rating']]
                .sort_values(by='Predicted Rating', ascending=False)
                .head(top_n)
                .reset_index(drop=True)
            )
        except Exception as e:
            st.error(f"Error running ML code: {e}")

 # --- Scenario 5: Statistical Insights ---
if scenario == "Scenario 5- Statistical Insights by Genre (Agreement %)":
    st.markdown('<h3 style="color:green;">Scenario 5 (Agreement % per Genre):</h3>', unsafe_allow_html=True)
    st.write("""
    This analysis measures how often my ratings align with IMDb ratings **within a tolerance band of ±1 point**.  
    Results are grouped by genre, showing agreements, disagreements, and overall percentages.
    """)

    if st.button("Run Statistical Analysis", key="run_stats"):
        try:
            # Merge IMDb and My Ratings
            df_compare = IMDB_Ratings.merge(
                My_Ratings[['Movie ID','Your Rating']],
                on='Movie ID', how='inner'
            )

            # Calculate agreement (±1 tolerance)
            df_compare['Agreement'] = (
                (df_compare['Your Rating'] - df_compare['IMDb Rating']).abs() <= 1
            )

            # Aggregate per genre
            genre_agreement = (
                df_compare.groupby('Genre')
                .agg(
                    Total_Movies=('Movie ID','count'),
                    Agreements=('Agreement','sum')
                )
                .reset_index()
            )
            genre_agreement['Disagreements'] = (
                genre_agreement['Total_Movies'] - genre_agreement['Agreements']
            )
            genre_agreement['Agreement_%'] = (
                genre_agreement['Agreements'] / genre_agreement['Total_Movies'] * 100
            ).round(2)

            # Show table
            st.write("### Agreement % per Genre (±1 Tolerance)")
            st.dataframe(
                genre_agreement.sort_values(by='Agreement_%', ascending=False),
                width="stretch",
                height=500
            )

        except Exception as e:
            st.error(f"Error calculating agreement stats: {e}")
            
# --- Scenario 5: Statistical Insights ---
if scenario == "Scenario 5- Statistical Insights by Genre (Agreement %)":
    st.markdown('<h3 style="color:green;">Scenario 5 (Agreement % per Genre):</h3>', unsafe_allow_html=True)
    st.write("""
    This analysis measures how often my ratings align with IMDb ratings **within a tolerance band of ±1 point**.  
    Results are grouped by genre, showing agreements, disagreements, and overall percentages.
    """)

    if st.button("Run Statistical Analysis", key="run_stats"):
        try:
            # Merge IMDb and My Ratings
            df_compare = IMDB_Ratings.merge(
                My_Ratings[['Movie ID','Your Rating']],
                on='Movie ID', how='inner'
            )

            # Calculate agreement (±1 tolerance)
            df_compare['Agreement'] = (
                (df_compare['Your Rating'] - df_compare['IMDb Rating']).abs() <= 1
            )

            # Aggregate per genre
            genre_agreement = (
                df_compare.groupby('Genre')
                .agg(
                    Total_Movies=('Movie ID','count'),
                    Agreements=('Agreement','sum')
                )
                .reset_index()
            )
            genre_agreement['Disagreements'] = (
                genre_agreement['Total_Movies'] - genre_agreement['Agreements']
            )
            genre_agreement['Agreement_%'] = (
                genre_agreement['Agreements'] / genre_agreement['Total_Movies'] * 100
            ).round(2)

            # Show table
            st.write("### Agreement % per Genre (±1 Tolerance)")
            st.dataframe(
                genre_agreement.sort_values(by='Agreement_%', ascending=False),
                width="stretch",
                height=500
            )

        except Exception as e:
            st.error(f"Error calculating agreement stats: {e}")
