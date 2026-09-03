"""
Offline training pipeline for the ratings-prediction model.

Trains a RandomForestRegressor on My_Ratings, evaluates it with
cross-validation, uploads the fitted model to Supabase Storage, and logs
the run (with its validation score) to the `model_runs` table. If the new
model's cross-validated RMSE beats the current production model, it is
promoted (is_current = true) and the previous production model is
demoted.

This is what lets the Streamlit app treat "the current model" as a
versioned, validated artifact it downloads and serves, instead of
something retrained from scratch on every button click.

Required environment variables:
    SUPABASE_URL
    SUPABASE_KEY            service_role key - needed to write model_runs
                             and upload to Storage regardless of RLS policy

Optional:
    IMDB_XLSX_PATH           defaults to "imdbratings.xlsx"
    MY_RATINGS_XLSX_PATH     defaults to "myratings.xlsx"
    GITHUB_SHA               auto-set by GitHub Actions; recorded for traceability

Requires a Supabase Storage bucket named "models" (create it once via the
Supabase dashboard: Storage -> New bucket -> name "models", private) and
the model_runs table (see model_runs_schema.sql).

Usage:
    python scripts/train_model.py
"""
import os
import sys
import tempfile
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from supabase import create_client

MODEL_BUCKET = "models"
CATEGORICAL_FEATURES = ["Genre", "Director"]
NUMERICAL_FEATURES = ["IMDb Rating", "Num Votes", "Year"]


def build_training_frame(imdb_path: str, my_ratings_path: str) -> pd.DataFrame:
    """Same join/feature set the Streamlit app's scenarios 10/11/14 already
    use, so a model trained here is a drop-in replacement for the one they
    used to train live."""
    imdb = pd.read_excel(imdb_path)
    mine = pd.read_excel(my_ratings_path)
    df = imdb.merge(mine[["Movie ID", "Your Rating"]], on="Movie ID", how="inner")
    return df.dropna(subset=CATEGORICAL_FEATURES + NUMERICAL_FEATURES + ["Your Rating"])


def train_and_evaluate(df: pd.DataFrame):
    X = df[CATEGORICAL_FEATURES + NUMERICAL_FEATURES]
    y = df["Your Rating"]

    preprocessor = ColumnTransformer(transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ("num", "passthrough", NUMERICAL_FEATURES),
    ])
    model = Pipeline([
        ("prep", preprocessor),
        ("reg", RandomForestRegressor(n_estimators=200, random_state=42)),
    ])

    cv = KFold(n_splits=min(5, len(df)), shuffle=True, random_state=42)
    scores = -cross_val_score(model, X, y, cv=cv, scoring="neg_root_mean_squared_error")
    model.fit(X, y)  # final fit on all labeled data for the artifact we ship
    return model, float(np.mean(scores)), float(np.std(scores))


def is_better(new_rmse: float, old_rmse) -> bool:
    """Lower RMSE wins. A model with no prior champion always wins.
    Pure function on purpose, so it's cheap to unit test without touching
    Supabase or scikit-learn at all - see tests/test_train_model.py."""
    if old_rmse is None:
        return True
    return new_rmse < old_rmse


def main() -> int:
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_KEY"]
    imdb_path = os.environ.get("IMDB_XLSX_PATH", "imdbratings.xlsx")
    my_ratings_path = os.environ.get("MY_RATINGS_XLSX_PATH", "myratings.xlsx")
    git_sha = os.environ.get("GITHUB_SHA", "local")

    supabase = create_client(supabase_url, supabase_key)

    df = build_training_frame(imdb_path, my_ratings_path)
    if len(df) < 10:
        print(f"Only {len(df)} usable training rows - need at least 10. Aborting.")
        return 1

    model, rmse_mean, rmse_std = train_and_evaluate(df)

    timestamp = datetime.now(timezone.utc)
    storage_path = f"model_{timestamp.strftime('%Y%m%dT%H%M%SZ')}.joblib"

    with tempfile.NamedTemporaryFile(suffix=".joblib") as tmp:
        joblib.dump(model, tmp.name)
        tmp.seek(0)
        # NOTE: supabase-py's storage upload signature has shifted across
        # versions (some accept a filepath string, some want raw bytes).
        # Check the installed `supabase` package version against its docs
        # if this line errors - the rest of the pipeline doesn't depend on
        # exactly how the bytes get there.
        supabase.storage.from_(MODEL_BUCKET).upload(
            storage_path, tmp.name, {"content-type": "application/octet-stream"}
        )

    # Find the current production model's score, if any, to decide promotion.
    current = (
        supabase.table("model_runs")
        .select("id, cv_rmse_mean")
        .eq("is_current", True)
        .limit(1)
        .execute()
    )
    old_rmse = current.data[0]["cv_rmse_mean"] if current.data else None
    promote = is_better(rmse_mean, old_rmse)

    supabase.table("model_runs").insert({
        "trained_at": timestamp.isoformat(),
        "git_sha": git_sha,
        "n_training_movies": len(df),
        "features": ", ".join(CATEGORICAL_FEATURES + NUMERICAL_FEATURES),
        "cv_rmse_mean": round(rmse_mean, 4),
        "cv_rmse_std": round(rmse_std, 4),
        "storage_path": storage_path,
        "is_current": promote,
    }).execute()

    if promote:
        if current.data:
            supabase.table("model_runs").update({"is_current": False}).eq(
                "id", current.data[0]["id"]
            ).execute()
        old_str = f"{old_rmse:.3f}" if old_rmse is not None else "none"
        print(f"New model PROMOTED to production: RMSE {rmse_mean:.3f} (previous: {old_str}).")
    else:
        print(
            f"New model trained but NOT promoted: RMSE {rmse_mean:.3f} did not "
            f"beat current production RMSE {old_rmse:.3f}. Logged for the record only."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
