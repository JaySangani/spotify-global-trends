# Data Setup Instructions

The raw dataset is not included in this repository because it exceeds GitHub's 100MB file limit and is owned by the original Kaggle publisher. Follow these steps to set it up locally.

---

## Step 1 — Create a free Kaggle account

Go to [kaggle.com](https://www.kaggle.com) and sign up. It is free.

---

## Step 2 — Download the dataset

Go to this URL and click Download:

```
https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated
```

The downloaded file will be called `universal_top_spotify_songs.csv` (approximately 500MB).

---

## Step 3 — Place the file in the correct location

Move the downloaded file to:

```
data/universal_top_spotify_songs.csv
```

Your folder structure should look like:

```
spotify-global-trends/
├── data/
│   ├── universal_top_spotify_songs.csv   ← place it here
│   └── clean/                            ← output goes here
```

---

## Step 4 — Run the cleaning script

```bash
conda run python spotify_clean.py
```

Or if you are not using Anaconda:

```bash
python spotify_clean.py
```

The script will produce 4 clean CSV files in `data/clean/` — these are what Tableau connects to.

---

## About the dataset

- **Publisher:** asaniczka on Kaggle
- **Coverage:** Top 50 songs per day across 73 countries
- **Updated:** Daily
- **Columns:** song name, artists, daily rank, country, popularity score, audio features (danceability, energy, valence, tempo, etc.)
- **License:** Check the Kaggle dataset page for current licensing terms
