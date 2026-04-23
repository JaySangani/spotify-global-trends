# Sounds of the World — Global Spotify Trends Dashboard

A business analysis and data visualisation project exploring what the world is listening to on Spotify right now — built on daily chart data across 73 countries.

![Dashboard Preview](dashboard/dashboard_screenshot.png)

[View Live Dashboard](#) <!-- Replace with Tableau Public link once published -->

---

## Business problem

Music platforms, labels, and marketers need to understand how listening habits differ across countries and what audio characteristics drive a song to the top of the charts. Without consolidated visibility across markets, decisions about artist promotion, regional targeting, and playlist curation are based on guesswork.

This project simulates a BA engagement where I analysed global streaming behaviour to surface patterns in song popularity, audio features, and regional music trends.

---

## What I delivered

| Artefact | Location | Description |
|---|---|---|
| Tableau Dashboard | Live link above | 3-tab interactive dashboard — world map, audio features, trends |
| Python Cleaning Script | `spotify_clean.py` | Reduces 500MB raw data to 4 lean Tableau-ready CSVs |
| Cleaned Datasets | `data/clean/` | Pre-aggregated CSVs for each dashboard tab |

---

## Dashboard tabs

1. **Where is music trending?** — World map showing avg popularity by country, top song per country, Top N songs bar chart
2. **What makes a hit song?** — Audio features radar chart, danceability vs popularity scatter plot, genre breakdown
3. **How do rankings move?** — Daily rank movement for top 50 songs over 90 days

---

## Key findings

- BIRDS OF A FEATHER by Billie Eilish is the most popular song globally across the dataset period (March to June 2025)
- Danceability and energy are the strongest audio predictors of chart performance
- Latin music dominates in South America and parts of Europe while English-language pop leads in Anglo markets
- 72 countries tracked with meaningful variation in regional preferences

---

## Dataset

**Source:** [Top Spotify Songs in 73 Countries — Kaggle (asaniczka)](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated)

See `DATA.md` for full download and setup instructions.

**Coverage:** March 2025 to present (updated daily on Kaggle)
**Raw size:** ~500MB (not included in repo — see DATA.md)
**Clean size:** <1MB after aggregation

---

## Tools used

- **Python** — pandas for data cleaning and aggregation
- **Tableau Public** — dashboard development and publishing

---

## How to reproduce

1. Download the raw dataset from Kaggle (see `DATA.md`)
2. Place the file at `data/universal_top_spotify_songs.csv`
3. Run `conda run python spotify_clean.py`
4. Open Tableau and connect to the files in `data/clean/`

---

## Folder structure

```
spotify-global-trends/
├── README.md
├── DATA.md
├── .gitignore
├── spotify_clean.py
└── data/
    └── clean/
        ├── tab1_world_map.csv
        ├── tab1_country_summary.csv
        ├── tab2_audio_features.csv
        └── tab3_trends.csv
```

---

*Part of my BA portfolio — see also: [supply-chain-analytics](https://github.com/JaySangani/supply-chain-analytics)*
