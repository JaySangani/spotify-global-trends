"""
Spotify Global Trends — Data Cleaning and Preparation
Author: Jay Sangani
Project: Sounds of the World — Global Spotify Trends Dashboard
Dataset: Top Spotify Songs in 73 Countries (Daily Updated) — Kaggle asaniczka

This script reads the large raw CSV and produces 3 clean, Tableau-ready files:
  - tab1_world_map.csv       — for the world map and top songs tab
  - tab2_audio_features.csv  — for the radar chart and scatter plot tab
  - tab3_trends.csv          — for the rank movement over time tab
"""

import pandas as pd
import numpy as np
import os

# ── Configuration ────────────────────────────────────────────────────────
INPUT_FILE = "data/universal_top_spotify_songs.csv"
OUTPUT_DIR = "data/clean"
DAYS_TO_KEEP = 90       # keep last 90 days — current and manageable
TOP_N_SONGS  = 200      # keep top N unique songs by avg popularity

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 1. Load raw data ──────────────────────────────────────────────────────
print("Loading raw data — this may take 30 to 60 seconds for a 500MB file...")
df = pd.read_csv(INPUT_FILE, low_memory=False)
print(f"Raw shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Columns: {df.columns.tolist()}")

# ── 2. Parse and filter dates ─────────────────────────────────────────────
print("\nParsing dates...")
df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="coerce")
df["album_release_date"] = pd.to_datetime(df["album_release_date"], errors="coerce")

# Keep only the most recent 90 days
cutoff_date = df["snapshot_date"].max() - pd.Timedelta(days=DAYS_TO_KEEP)
df = df[df["snapshot_date"] >= cutoff_date]
print(f"After date filter ({DAYS_TO_KEEP} days): {df.shape[0]:,} rows")
print(f"Date range: {df['snapshot_date'].min().date()} to {df['snapshot_date'].max().date()}")

# ── 3. Basic cleaning ─────────────────────────────────────────────────────
print("\nCleaning data...")

# Standardise country column name (may vary)
if "country" in df.columns:
    country_col = "country"
elif "country_name" in df.columns:
    country_col = "country_name"
else:
    # Find it
    country_col = [c for c in df.columns if "country" in c.lower()][0]

print(f"Country column: {country_col}")
print(f"Countries: {df[country_col].nunique()}")
print(f"Sample countries: {df[country_col].unique()[:8].tolist()}")

# Clean text fields
df["name"]    = df["name"].astype(str).str.strip()
df["artists"] = df["artists"].astype(str).str.strip()

# Extract year from album release date
df["release_year"] = df["album_release_date"].dt.year

# Extract just the date part of snapshot
df["date"] = df["snapshot_date"].dt.date

# Audio feature columns — confirm which exist
audio_cols = ["danceability", "energy", "speechiness",
              "acousticness", "instrumentalness", "liveness",
              "valence", "tempo", "loudness"]
audio_cols = [c for c in audio_cols if c in df.columns]
print(f"Audio feature columns found: {audio_cols}")

# ── 4. TAB 1 — World map and top songs ────────────────────────────────────
print("\nBuilding Tab 1: World map and top songs...")

# Average popularity per song per country over the 90 days
tab1 = df.groupby([country_col, "name", "artists"]).agg(
    avg_popularity  = ("popularity",  "mean"),
    avg_daily_rank  = ("daily_rank",  "mean"),
    appearances     = ("daily_rank",  "count"),
    release_year    = ("release_year","first"),
    is_explicit     = ("is_explicit", "first")
).reset_index()

tab1 = tab1.round(2)

# Also create a country-level summary for the map
country_summary = df.groupby(country_col).agg(
    avg_popularity    = ("popularity",  "mean"),
    total_appearances = ("daily_rank",  "count"),
    unique_songs      = ("name",        "nunique"),
    top_song          = ("name",        lambda x: x.value_counts().index[0]),
    top_artist        = ("artists",     lambda x: x.value_counts().index[0])
).reset_index().round(2)

tab1.to_csv(f"{OUTPUT_DIR}/tab1_world_map.csv", index=False)
country_summary.to_csv(f"{OUTPUT_DIR}/tab1_country_summary.csv", index=False)
print(f"Tab 1 saved: {len(tab1):,} rows (song-country combos)")
print(f"Country summary: {len(country_summary)} countries")

# ── 5. TAB 2 — Audio features ─────────────────────────────────────────────
print("\nBuilding Tab 2: Audio features...")

# One row per unique song with avg audio features and avg popularity
tab2 = df.groupby(["name", "artists"]).agg(
    avg_popularity      = ("popularity",         "mean"),
    avg_rank            = ("daily_rank",         "mean"),
    country_count       = (country_col,          "nunique"),
    release_year        = ("release_year",       "first"),
    is_explicit         = ("is_explicit",        "first"),
    **{f"avg_{col}": (col, "mean") for col in audio_cols}
).reset_index()

# Keep top N songs by popularity
tab2 = tab2.nlargest(TOP_N_SONGS, "avg_popularity").round(4)

tab2.to_csv(f"{OUTPUT_DIR}/tab2_audio_features.csv", index=False)
print(f"Tab 2 saved: {len(tab2):,} songs with audio features")

# ── 6. TAB 3 — Trends over time ───────────────────────────────────────────
print("\nBuilding Tab 3: Trends over time...")

# Daily global rank for top songs (averaged across countries per day)
# Get the top 50 songs by overall popularity first
top_songs = (df.groupby("name")["popularity"]
             .mean()
             .nlargest(50)
             .index.tolist())

tab3 = (df[df["name"].isin(top_songs)]
        .groupby(["date", "name", "artists"])
        .agg(
            avg_rank       = ("daily_rank",  "mean"),
            avg_popularity = ("popularity",  "mean"),
            country_count  = (country_col,   "nunique")
        )
        .reset_index()
        .round(2))

tab3["date"] = tab3["date"].astype(str)
tab3.to_csv(f"{OUTPUT_DIR}/tab3_trends.csv", index=False)
print(f"Tab 3 saved: {len(tab3):,} rows (daily trends for top 50 songs)")

# ── 7. Summary ────────────────────────────────────────────────────────────
print("\n" + "="*50)
print("ALL FILES SAVED SUCCESSFULLY")
print("="*50)

for fname in os.listdir(OUTPUT_DIR):
    fpath = os.path.join(OUTPUT_DIR, fname)
    size_mb = os.path.getsize(fpath) / 1_000_000
    print(f"  {fname}: {size_mb:.2f} MB")

print("\nKey stats from your data:")
print(f"  Date range:       {df['snapshot_date'].min().date()} to {df['snapshot_date'].max().date()}")
print(f"  Countries:        {df[country_col].nunique()}")
print(f"  Unique songs:     {df['name'].nunique():,}")
print(f"  Unique artists:   {df['artists'].nunique():,}")
print(f"  Top song overall: {df.groupby('name')['popularity'].mean().idxmax()}")
print(f"  Top artist:       {df.groupby('artists')['popularity'].mean().idxmax()}")
print("\nNext step: open Tableau and connect to the 3 clean CSV files in data/clean/")