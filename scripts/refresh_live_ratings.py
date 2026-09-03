"""
Standalone refresher for the "Live Ratings Monitor" scenario.

Re-checks the Horror subset of IMDB_Ratings against OMDb and logs any rating
changes into the Supabase `films` table. Meant to run OUTSIDE Streamlit (e.g.
on a GitHub Actions schedule), so history keeps accumulating even when nobody
has the app open.

Required environment variables:
    SUPABASE_URL
    SUPABASE_KEY
    OMDB_API_KEY

Optional:
    IMDB_XLSX_PATH   defaults to "imdbratings.xlsx"

Usage:
    python scripts/refresh_live_ratings.py
"""
import os
import sys
from datetime import datetime, timezone

import pandas as pd
import requests
from supabase import create_client


def main() -> int:
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_KEY"]
    omdb_api_key = os.environ["OMDB_API_KEY"]
    xlsx_path = os.environ.get("IMDB_XLSX_PATH", "imdbratings.xlsx")

    supabase = create_client(supabase_url, supabase_key)

    imdb_ratings = pd.read_excel(xlsx_path)
    top250 = (
        imdb_ratings[imdb_ratings["Genre"].str.contains("Horror", case=False, na=False)]
        .sort_values(by="IMDb Rating", ascending=False)
        .head(250)
    )

    timestamp = datetime.now(timezone.utc).isoformat()
    records = []

    for _, row in top250.iterrows():
        movie_id = row["Movie ID"]
        static_rating = row["IMDb Rating"]

        try:
            resp = requests.get(
                "http://www.omdbapi.com/",
                params={"i": movie_id, "apikey": omdb_api_key},
                timeout=10,
            ).json()
        except requests.RequestException:
            continue

        if resp.get("Response") != "True":
            continue

        languages = [lang.strip().lower() for lang in resp.get("Language", "").split(",")]
        if "english" not in languages:
            continue

        live_rating = float(resp["imdbRating"]) if resp.get("imdbRating") else None
        if live_rating is None:
            continue

        rating_diff = live_rating - static_rating
        if rating_diff == 0:
            continue

        records.append({
            "movie_id": movie_id,
            "title": row["Title"],
            "imdb_rating_static": static_rating,
            "imdb_rating_live": live_rating,
            "rating_diff": rating_diff,
            "genre": row.get("Genre"),
            "director": row.get("Director"),
            "year": int(row["Year"]) if pd.notna(row.get("Year")) else None,
            "num_votes": row.get("Num Votes"),
            "language": ", ".join(lang.capitalize() for lang in languages),
            "checked_at": timestamp,
        })

    if records:
        supabase.table("films").insert(records).execute()
        print(f"Logged {len(records)} row(s) to Supabase at {timestamp}.")
    else:
        print("No rating changes found this run - nothing logged.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
