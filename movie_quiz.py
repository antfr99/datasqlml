import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb/SQL/PYTHON Data Project 🎬")
st.write("""
This is a small IMDb data project combining Python Packages (Pandas, PandasQL, Numpy , Streamlit , Sklearn , Scipy ), SQL, and GitHub.
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
        "Scenario 1 – Highlight Disagreements (SQL)",
        "Scenario 2 – Hybrid Recommendation (SQL)",
        "Scenario 3 – Top Unseen Films by Decade (SQL)",
        "Scenario 4 – Predict My Ratings (ML)",
        "Scenario 5 – Statistical Insights by Genre (Agreement %)",
        "Scenario 6 - Statistical Insights by Director (t-test)",
        "Scenario 7 — NLP Script Analysis (scene segmentation, character extraction, NER, sentiment, summary)."
    ]
)
# --- Scenario 1: SQL Playground ---
if scenario == "Scenario 1 – Highlight Disagreements (SQL)":
    st.markdown('<h3 style="color:green;">Scenario 1 (My Ratings vs IMDb)</h3>', unsafe_allow_html=True)
    st.write("Movies where my rating differs from IMDb by more than 2 points.")

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
    if st.button("Run SQL Query – Find my disagreements", key="run_sql1"):
        try:
            result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
            st.dataframe(result, width="stretch", height=800)
        except Exception as e:
            st.error(f"Error in SQL query: {e}")

# --- Scenario 2: SQL Playground ---
if scenario == "Scenario 2 – Hybrid Recommendation (SQL)":
    st.markdown('<h3 style="color:green;">Scenario 2 (Recommend Unseen Movies)</h3>', unsafe_allow_html=True)
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
    if st.button("Run SQL Query – Recommend movies", key="run_sql2"):
        try:
            result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
            st.dataframe(result, width="stretch", height=800)
        except Exception as e:
            st.error(f"Error in SQL query: {e}")

# --- Scenario 3: SQL Playground ---
if scenario == "Scenario 3 – Top Unseen Films by Decade (SQL)":
    st.markdown('<h3 style="color:green;">Scenario 3 (Decade Discovery – Top Unseen Films)</h3>', unsafe_allow_html=True)
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
    if st.button("Run SQL Query – Top unseen films", key="run_sql3"):
        try:
            result = ps.sqldf(user_query, {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings})
            st.dataframe(result, width="stretch", height=800)
        except Exception as e:
            st.error(f"Error in SQL query: {e}")

# --- Scenario 4: Python ML ---
if scenario == "Scenario 4 – Predict My Ratings (ML)":
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
if scenario == "Scenario 5 – Statistical Insights by Genre (Agreement %)":
    st.markdown('<h3 style="color:green;">Scenario 5 (Agreement % per Genre):</h3>', unsafe_allow_html=True)
    st.write("""
    This analysis measures how often my ratings align with IMDb ratings **within a tolerance band of ±1 point**.  
    Results are grouped by genre, showing agreements, disagreements, and overall percentages.
    """)

    stats_code = '''
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

# Add disagreements and percentages
genre_agreement['Disagreements'] = (
    genre_agreement['Total_Movies'] - genre_agreement['Agreements']
)
genre_agreement['Agreement_%'] = (
    genre_agreement['Agreements'] / genre_agreement['Total_Movies'] * 100
).round(2)

# Final result
genre_agreement.sort_values(by='Agreement_%', ascending=False)
'''

    # Editable code box
    user_stats_code = st.text_area("Python Statistical Code (editable)", stats_code, height=600)

    if st.button("Run Statistical Analysis", key="run_stats5"):
        try:
            # Run the code entered in the text area
            local_vars = {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings}
            exec(user_stats_code, {}, local_vars)

            # Retrieve dataframe if created
            if "genre_agreement" in local_vars:
                st.dataframe(local_vars["genre_agreement"], width="stretch", height=500)
            else:
                st.warning("No output dataframe named 'genre_agreement' was produced. Please check your code.")

        except Exception as e:
            st.error(f"Error running Statistical Analysis code: {e}")



# --- Scenario 6: Statistical Insights (t-test per Director) ---

# --- Scenario 6: Statistical Insights (t-test per Director) ---
if scenario == "Scenario 6 - Statistical Insights by Director (t-test)":
    st.markdown('<h3 style="color:green;">Scenario 6 (t-test per Director)</h3>', unsafe_allow_html=True)
    st.write("""
This analysis examines how my ratings compare with IMDb ratings for each director using a **paired t-test**.  
Directors with too few movies are ignored.
""")

    # Sidebar slider for minimum movies per director
    min_movies = st.sidebar.slider("Minimum movies per director for t-test", 2, 10, 5)

    # Editable t-test code
    ttest_code_director = f'''
from scipy.stats import ttest_rel
import numpy as np
import pandas as pd

# Merge IMDb and My Ratings
df_ttest = IMDB_Ratings.merge(
    My_Ratings[['Movie ID','Your Rating']],
    on='Movie ID', how='inner'
)

results = []

for director, group in df_ttest.groupby('Director'):
    n = len(group)
    if n >= {min_movies}:
        differences = group['Your Rating'] - group['IMDb Rating']

        # Handle zero variance (all differences identical)
        if differences.std() == 0:
            stat, pval = np.nan, np.nan
            interpretation = "All differences identical — t-test undefined"
        else:
            stat, pval = ttest_rel(group['Your Rating'], group['IMDb Rating'])
            if pval < 0.05:
                if n <= 2*{min_movies}:
                    interpretation = "Significant (p < 0.05) — small sample, interpret cautiously"
                else:
                    interpretation = "Significant (p < 0.05)"
            else:
                interpretation = "Not Significant"

        results.append({{
            "Director": director,
            "Num_Movies": n,
            "Mean_IMDb": group['IMDb Rating'].mean().round(2),
            "Mean_Mine": group['Your Rating'].mean().round(2),
            "t_statistic": round(stat, 3) if not np.isnan(stat) else np.nan,
            "p_value": round(pval, 4) if not np.isnan(pval) else np.nan,
            "Interpretation": interpretation
        }})

# Convert results to DataFrame
df_results = pd.DataFrame(results)
df_results = df_results.sort_values(by="p_value")
'''

    user_ttest_code_director = st.text_area("Python t-test per Director Code (editable)", ttest_code_director, height=650)

    if st.button("Run t-test Analysis", key="run_ttest_director6"):
        try:
            local_vars = {"IMDB_Ratings": IMDB_Ratings, "My_Ratings": My_Ratings}
            exec(user_ttest_code_director, {}, local_vars)

            if "df_results" in local_vars:
                st.dataframe(local_vars["df_results"], width="stretch", height=500)
            else:
                st.warning("No dataframe named 'df_results' was produced. Please check your code.")

        except Exception as e:
            st.error(f"Error running t-test analysis: {e}")

# --- Scenario 7 - NLP Script Analysis ---
if scenario == "Scenario 7 — NLP Script Analysis (scene segmentation, character extraction, NER, sentiment, summary).":
    st.markdown('<h3 style="color:green;">Scenario 7 — NLP Script Analysis</h3>', unsafe_allow_html=True)

    import re
    import pandas as pd

    # Optional NLP libs
    try:
        import docx  # python-docx
    except Exception:
        docx = None

    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        spacy = None
        nlp = None

    try:
        from textblob import TextBlob
    except Exception:
        TextBlob = None

    # Optional summarizer (transformers)
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization")
    except Exception:
        summarizer = None

    # --- Upload / paste input ---
    upload = st.file_uploader("Upload a .docx or .txt script file", type=["docx", "txt"])
    pasted = st.text_area("Or paste the script text here")

    def read_docx_file(uploaded_file):
        if docx is None:
            st.warning("python-docx not installed — please paste text or install python-docx.")
            return ""
        doc = docx.Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs)

    text = ""
    if pasted.strip():
        text = pasted
    elif upload is not None:
        if upload.type == "text/plain":
            text = upload.getvalue().decode("utf-8")
        else:
            text = read_docx_file(upload)

    # --- Run only on button click ---
    if st.button("Analyse Script"):
        if not text:
            st.warning("Please upload or paste a script first.")
        else:
            # Sidebar options
            min_scene_len = st.sidebar.slider("Minimum words in scene to keep", 5, 200, 8)
            preserve_case = st.sidebar.checkbox("Preserve original case", value=False)
            do_ner = st.sidebar.checkbox("Run spaCy NER", value=True if nlp else False)
            do_sentiment = st.sidebar.checkbox("Run sentiment (TextBlob)", value=True if TextBlob else False)
            do_summary = st.sidebar.checkbox("Generate summaries (transformers)", value=True if summarizer else False)

            # --- Cleaning & normalization ---
            def normalize_text(t, preserve_case=False):
                t = t.replace("\r\n", "\n").replace("\r", "\n")
                if not preserve_case:
                    t = t.strip()
                return t

            text_clean = normalize_text(text, preserve_case=preserve_case)

            # --- Scene segmentation ---
            scene_split_regex = re.compile(r'(?=(?:^|\n)(INT\.|EXT\.|FADE IN:|CUT TO:|SCENE|EXT\.)\b)', flags=re.IGNORECASE)
            parts = [p.strip() for p in scene_split_regex.split(text_clean)]
            scenes = []
            if len(parts) == 1:
                scenes = [parts[0]]
            else:
                i = 0
                while i < len(parts):
                    marker = parts[i]
                    if marker.strip() == "":
                        i += 1
                        continue
                    if re.match(r'^(INT\.|EXT\.|FADE IN:|CUT TO:|SCENE|EXT\.)', marker, flags=re.IGNORECASE):
                        header = marker.strip()
                        body = parts[i+1] if i+1 < len(parts) else ""
                        scenes.append((header, body.strip()))
                        i += 2
                    else:
                        scenes.append(("UNKNOWN", parts[i].strip()))
                        i += 1

            # Filter tiny scenes
            scenes = [(h, b) for (h, b) in scenes if len(b.split()) >= min_scene_len]

            st.write(f"Detected **{len(scenes)}** scenes (after filtering).")

            # --- Character extraction ---
            def extract_characters_from_scene(body_text):
                names = set()
                for line in body_text.splitlines():
                    s = line.strip()
                    if len(s) > 0 and s.isupper() and 1 <= len(s.split()) <= 4 and len(s) < 40:
                        s2 = re.sub(r'[^A-Z0-9\s\-\']', '', s)
                        if len(s2) > 0:
                            names.add(s2)
                return sorted(names)

            scene_records = []
            all_characters = set()
            for idx, (header, body) in enumerate(scenes, start=1):
                chars = extract_characters_from_scene(body)
                all_characters.update(chars)

                # NER
                ner_entities = []
                if do_ner and nlp:
                    doc = nlp(body)
                    ner_entities = [(ent.text, ent.label_) for ent in doc.ents]

                # Sentiment
                sentiment_polarity = None
                if do_sentiment and TextBlob:
                    tb = TextBlob(body)
                    sentiment_polarity = round(tb.sentiment.polarity, 3)

                # Summary
                summary = None
                if do_summary and summarizer:
                    try:
                        snippet = body[:2000]
                        summ = summarizer(snippet, max_length=60, min_length=15, do_sample=False)
                        summary = summ[0]['summary_text']
                    except Exception:
                        summary = None

                scene_records.append({
                    "SceneIndex": idx,
                    "Header": header,
                    "NumWords": len(body.split()),
                    "Characters": ", ".join(chars) if chars else "",
                    "NER": str(ner_entities) if ner_entities else "",
                    "Sentiment": sentiment_polarity,
                    "Summary": summary or ""
                })

            df_scenes = pd.DataFrame(scene_records)

            # Show results
            st.subheader("Scenes table")
            st.dataframe(df_scenes)

            st.subheader("Top detected characters")
            st.write(sorted(list(all_characters))[:50])

            # Export
            csv = df_scenes.to_csv(index=False).encode("utf-8")
            st.download_button("Download scenes CSV", csv, file_name="script_scenes.csv", mime="text/csv")
