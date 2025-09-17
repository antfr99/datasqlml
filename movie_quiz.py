import streamlit as st
import pandas as pd
import pandasql as ps

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("IMDb/SQL/PYTHON Data Project 🎬")
st.write("""
This is a small IMDb data project combining Python Packages (Pandas, PandasQL, Numpy , Streamlit , Sklearn , Scipy , Spacy, Textblob ), SQL, and GitHub.
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
        "Scenario 7 — Review Analysis (NER, Sentiment, Keywords, Summary)"
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




# --- Remove subprocess and sys imports related to runtime download ---

import spacy
from textblob import TextBlob
import pandas as pd
import streamlit as st

if scenario == "Scenario 7 — Review Analysis (NER, Sentiment, Keywords, Summary)":
    st.header("Scenario 7 — Film Review Analysis - Mother!2017")

    # --- Load spaCy model safely ---
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = None
        st.warning("spaCy model not available. NER will be skipped.")


    # --- All reviews stored in a multi-line string ---
    reviews_text = """
Religious allegories abound but really it's just pretentious nonsense
Now I'm not one to disparage the director, I liked Requiem for a Dream and loved Black Swan, but this is a stinker and just simply boring. It's all just packed full of cod biblical allegories spread thickly throughout which tries to twist between different types of horror genres, but leaved me unintrigued. 
Granted the settings, claustrophobic direction and acting are top notch but it shouldn't mask for what otherwise is a poor uninteresting movie. It unsettles and bores, way too much to care, and as the ending dragged on I was left increasingly frustrated as it refused to just shut up shop. 
It's totally split opinion from what I've seen so far, and you'll struggle to find anyone in the middle on this one. In fairness, some credit to the film studios for risking this effort in launching it into mainstream cinemas but without the director it would have rightfully languished on cable late night showings.
There's no point going anymore into this. I simply hated it, and that despite being a major admirer of offbeat horror and psychological movies, but this isn't in the same league as for example Raw or Get Out, which is a shame. I'd recommend you pass on this there are far better films out there to go watch.
Aronofsky's mother! will be hated by many, but loved by a precious few

Horrifying. Just.. horrifying. Aronofsky really got me with this one. Not only did he manage to grab me on an intellectual level, but also on an emotional one...
# (Include all remaining reviews here, each separated by an empty line)

Usually this is where I put my plot description but it's best that you go into Darren Aronofsky's latest knowing as little as possible. Lets just say that Jennifer Lawrence and Javier Bardem are living in a large house all alone when a surprise visit sets them off into madness.
It really shocks me that Paramount would try to push MOTHER! onto the masses. For starters, the majority of moviegoers today do not want to think and they certainly don't want to see a movie where everything isn't explained. In fact, most people need everything explained in the trailer before they'll even go see a movie. A movie like MOTHER! is something that never explains itself and it constantly keeps you guessing from one scene to the next. What's it about? It's really hard to say as every viewer is going to come away with something different. With all of that said, it's easy to see why the film bombed at the box office and why those who did see it gave it a F rating.
what I loved most about this movie is that the setting is just so perfect. You've got a large beautiful house out in the middle of nowhere and it's surrounded by beautiful grass and trees. From the very first scene we can just tell that something isn't quite right and Aronofsky puts us in this beautiful place with confusing surroundings. What makes the film so special is the fact that nothing is ever explained and with each new plot twist your brain just becomes more confused as to what's going on. We know something is happening and we know something bad is going to happen but you're constantly trying to guess what.
Of course, a movie like this wouldn't work without a terrific cast to pull it off. Lawrence turns in another terrific performance and I thought she as fabulous at showing how fractured this character was. We're often questioning her mental state and I thought Lawrence managed to make you feel for the character and go along with her confusion to everything that is happening. Bardem actually steals the show with his fiery performance and I really loved the rage and anger he brought to the film as well as another side that I won't spoil to prevent giving away aspects of the plot. Both Ed Harris and Michelle Pfeiffer were also terrific but, again, I'll hold off commenting more to prevent plot points.
The cinematography is terrific and on a technical level the film is quite flawless. The story is a very interesting one and one that keeps you guessing throughout. The performances just seal the deal. With that said, the film certainly goes downright insane at times and the ending is just one that will have you staggering out of the theater. I must say that I thought the finale went on a bit too long and that it would have worked better had it been edited down a bit. Still, MOTHER! is a film that I really loved and one that I really respected but at the same time I'm not sure who I'd recommend it to.

Went to the first matinée available locally and I am still thinking the picture over. Will definitely see this one again, if it hasn't left the theatre abruptly. I was certainly horrified by the film, which is a good thing, as I had assumed it was a horror picture. It is, of course, much more than that. Nonetheless, it is NOT The Conjuring or Get Out (both good films, for sure), so just be warned.
By now you are aware that the film has been controversial, also a good thing. Jennifer Lawrence does a fine job and her career is certainly not going to suffer for her performance. I am not exactly a JLaw "fan" (could live without the Hunger Games), although I will pay closer attention to her future performances, especially if she pulls off more roles like this one (really liked Winter's Bone, by the way). As I understand the Hollywood scene, it is a respectable personal decision to take on a challenging role in an avant garde picture, especially if you have already banked serious money from popular roles in blockbusters. Javier Bardem, Michelle Pfeiffer, and Ed Harris also do their respective parts justice--a well-acted film by A-listers, overall. Camera work and special effects are also impressive.
The story is genuinely disturbing in a Requiem for a Dream way, so don't go if you can't handle that sort of thing. Some of the violence is, indeed, OVER THE TOP. Seriously, not for the faint of heart. Aside from the biblical allegory stuff, I found the character portrayals creepy as hell in a (sur?)realistic David Lynch-esque way. Hell is other people!
I applaud Mr. Aronofsky for keeping his vision intact all the way to the big screen. For reference, I just don't need any more movies based on superheros, comic books (except The Tenth or Gen 13), children's cartoons, vampires fighting werewolves, or horror stick about unfriending weirdos on facebook. 
You will have to make up your own mind on this one, so please do just that. Even if you end up despising the film, try to remember that, to quote Rob Zombie, "Art's Not Safe."

A married couple live in an isolated country house. He is a celebrated poet, suffering from writer's block, and she is working on renovating the house. Then a guest, a stranger, suddenly drops in and nothing will ever be the same again. 
Written and directed by Darren Aronofsky who gave us masterpieces like 'The Wrestler' and 'Requiem for a Dream', as well as the excellent 'Black Swan'. The fact that he wrote and directed this was the only reason I watched it, hoping that he was back to the form of those movies as his previous movie was the craptacular-beyond-belief 'Noah'.
Unfortunately, no, he isn't, though initially there was a glimmer of hope. The movie started interestingly enough, with some decent character development and some interesting themes. However, from the outset it was slow, plus there were signs this wasn't going to be a character-based drama but something symbolic, and pretentious.
Plus it was annoying. The only likeable character was Jennifer Lawrence's. Javier Bardem's was selfish and egotistical and every single other character was incredibly irritating. 
Still, I was hoping this would all develop into something interesting and profound. Wrong again. It develops into anarchy and some sort of badly-thought-out horror movie, and the annoyance factor gets pushed to the max. Of course, it's all meant to be symbolic, but figuring out everything would require you to think about the movie, and do so you would have had to have concentrated all through the tidal wave of excrement that was the movie.
Pretentious and annoying, and evidence that, sadly, Darren Aronofsky has run out of ideas.

I have been going to the movies for 45 years. This is, hands down, the worst movie I have ever seen. I mean, I hated this movie. Plan 9 From Outer Space and The Room were at least entertaining. This is like being locked in a cell with a stoned college student who can't shut up and thinks that every opinion they have, is the final word on a subject for 2 hours. Jennifer Lawrence should stick to roles that require her to paint herself blue or shoot arrows. Darren Aronofsky wants to be Luis Buñuel but he's closer to Uwe Boll. He cites The Exterminating Angel as the inspiration for Mother! I agree, in the sense that I did feel like one of the dinner guests who can't leave in Buñuel's classic during the course of watching Mother after paying 13 bucks to see this pretentious, heavy handed waste of time. Do yourself a favor, don't go see this movie, you won't get the 2 hours of your life back if you do. When it shows up on The Movie Channel playing at 3 in the morning in a couple of months, don't even set your DVR to record it. There are infomercials about gardening tools on at the same time, that are much more entertaining to watch that this.

I thought this was worth its salt even though it did tend towards cliché as it wore on. The disappointing aspect of this film is that Jennifer Lawrence somehow portrays an ego that is beyond the character. It's a kind of "you know that I know I'm only acting this and the real movie is me" that seems to have perpetuated in every film she had made since Silver linings Playbook, bar X-Men (when she was covered in paint and having to "live in" the previous "humble" shoes of Rebecca Romijn) and American Hustle (where she was greedy White Trash). She needs a director who can "humble her down", in the same way Eastwood did for Jolie in Changeling, so that her ego is less of a distraction for her acting.

Where to start - I've literally just finished watching this and spent the last hour questioning if I had been transported to another universe.
This movie had all the potential to be something great, from the cast to the secluded creepy setting - but no, we got almost 2 hours of the what could only be described as one of those brainwashing experimental videos where you have no idea what's going on.
If you like movies which make you feel uneasy, and make you think you're going mad then this might be the movies for you. Otherwise, I wouldn't bother.
Edit:So after having a day or so to ponder over the meaning of this movie - I've changed my rating and edited my review based on what I have come to know.
I can now say that once you understand the characters and why they represent, you'll understand the meaning and it could change your entire view of this movie.

    """

    # --- Convert multi-line text to list of reviews ---
    reviews = [r.strip() for r in reviews_text.split("\n\n") if r.strip()]

    st.write(f"Loaded **{len(reviews)}** reviews")

    # --- Ensure spaCy model is available ---
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        st.info("spaCy model not found. Downloading en_core_web_sm...")
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")

    review_records = []
    review_counter = 1
    for review in reviews:
        # Skip very short or empty reviews
        if len(review.split()) < 5 or review.strip() == "":
            continue

        tb = TextBlob(review)
        sentiment = tb.sentiment.polarity
        subjectivity = tb.sentiment.subjectivity

        ents = []
        if nlp:
            doc_nlp = nlp(review)
            ents = [ent.text for ent in doc_nlp.ents if ent.label_ in ["PERSON","ORG","WORK_OF_ART"]]

        review_records.append({
            "ReviewID": review_counter,
            "Words": len(review.split()),
            "Sentiment": round(sentiment, 3),
            "Subjectivity": round(subjectivity, 3),
            "Entities": ", ".join(set(ents)),
            "Snippet": review[:500] + ("..." if len(review) > 500 else "")
        })
        review_counter += 1

    df_reviews = pd.DataFrame(review_records)

    # Remove empty rows
    df_reviews = df_reviews[df_reviews['Snippet'].str.strip() != ""].reset_index(drop=True)

    # --- Filter ReviewID 1 to 8 ---
    df_reviews = df_reviews[df_reviews['ReviewID'].between(1, 8)].reset_index(drop=True)

    # --- Display table ---
    st.subheader("Reviews overview")
    st.dataframe(df_reviews, width="stretch", height=400)

    # --- Aggregate statistics ---
    st.subheader("Aggregate Insights")
    st.write(f"**Average sentiment:** {df_reviews['Sentiment'].mean():.3f}")
    st.write(f"**Average subjectivity:** {df_reviews['Subjectivity'].mean():.3f}")

    # --- Explanation ---
    st.markdown("""
    **What these metrics mean:**
    - **Sentiment**: ranges from -1 (negative) to +1 (positive). Shows if the review leans negative or positive.  
    - **Subjectivity**: ranges from 0 (objective/factual) to 1 (subjective/opinionated). High subjectivity means more personal impressions.  
    - **Entities**: names of people, organizations, or works of art automatically detected by spaCy.  
    """)

    # --- Full reviews in collapsible grey block ---
    st.markdown("---")
    with st.expander("Full Reviews (click to expand)"):
        for r in reviews:
            if len(r.split()) >= 5 and r.strip() != "":
                st.markdown(f"<div style='color:gray; padding:5px;'>{r}</div>", unsafe_allow_html=True)