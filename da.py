"""
Netflix Movies & TV Shows - Analysis Script
Designed to run in VS Code as a standalone Python script.

Outputs: PNG plots saved to ./plots/ and a summary CSV ./output/summary_stats.csv

Usage:
    python netflix_analysis.py --csv netflix_titles.csv

Requirements:
    pandas, matplotlib, seaborn, numpy
    Install: pip install pandas matplotlib seaborn numpy

This script performs cleaning, EDA, and saves plots for inclusion in a PPT or report.
"""

import argparse
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_dirs():
    os.makedirs(os.path.join(SCRIPT_DIR, "plots"), exist_ok=True)
    os.makedirs(os.path.join(SCRIPT_DIR, "output"), exist_ok=True)


def read_data(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found at {csv_path}")
        sys.exit(1)
    df = pd.read_csv(csv_path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    # Parse dates
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
        df["year_added"] = df["date_added"].dt.year
    else:
        df["year_added"] = np.nan

    # Fill missing simple text columns with 'Unknown'
    for col in ["director", "cast", "country", "rating"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Normalize 'type' column (Movie / TV Show)
    if "type" in df.columns:
        df["type"] = df["type"].str.strip()

    # Split listed_in into list (genres/categories)
    if "listed_in" in df.columns:
        df["listed_in"] = df["listed_in"].fillna("Unknown")
        df["genres_list"] = df["listed_in"].apply(lambda x: [g.strip() for g in str(x).split(",")])
    else:
        df["genres_list"] = [[] for _ in range(len(df))]

    # Parse duration: for Movies -> minutes; for TV Shows -> seasons
    def parse_duration(x):
        if pd.isna(x):
            return np.nan
        s = str(x).strip()
        # Examples: '90 min' or '2 Seasons' or '1 Season'
        try:
            if "min" in s:
                return int(s.split()[0])
            else:
                # seasons -> return number of seasons
                return int(s.split()[0])
        except Exception:
            return np.nan

    if "duration" in df.columns:
        df["duration_parsed"] = df["duration"].apply(parse_duration)
    else:
        df["duration_parsed"] = np.nan

    # Clean country: take first country if multiple listed
    if "country" in df.columns:
        df["primary_country"] = df["country"].apply(lambda x: str(x).split(",")[0].strip() if pd.notna(x) and x != "Unknown" else "Unknown")
    else:
        df["primary_country"] = "Unknown"

    return df


def plot_movies_vs_tv(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    order = df["type"].value_counts().index
    sns.countplot(data=df, x="type", order=order, ax=ax)
    ax.set_title("Movies vs TV Shows on Netflix")
    ax.set_xlabel("")
    ax.set_ylabel("Count")
    plt.tight_layout()
    path = os.path.join(SCRIPT_DIR, "plots", "movies_vs_tv.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved {path}")


def plot_top_genres(df: pd.DataFrame, top_n=12):
    # explode genres_list
    all_genres = Counter()
    for gl in df["genres_list"]:
        for g in gl:
            all_genres[g] += 1
    top = all_genres.most_common(top_n)
    genres, counts = zip(*top)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=list(counts), y=list(genres), ax=ax)
    ax.set_title(f"Top {top_n} Genres / Categories")
    ax.set_xlabel("Count")
    ax.set_ylabel("")
    plt.tight_layout()
    path = os.path.join(SCRIPT_DIR, "plots", "top_genres.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved {path}")


def plot_yearly_trend(df: pd.DataFrame):
    if "year_added" not in df.columns or df["year_added"].isna().all():
        print("No year_added information available to plot yearly trend.")
        return
    series = df["year_added"].dropna().astype(int).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    series.plot(ax=ax)
    ax.set_title("Content Added to Netflix Over Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Titles Added")
    plt.tight_layout()
    path = os.path.join(SCRIPT_DIR, "plots", "content_added_per_year.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved {path}")


def plot_top_countries(df: pd.DataFrame, top_n=10):
    counts = df["primary_country"].value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=counts.values, y=counts.index, ax=ax)
    ax.set_title(f"Top {top_n} Countries by Number of Titles")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("")
    plt.tight_layout()
    path = os.path.join(SCRIPT_DIR, "plots", "top_countries.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved {path}")


def plot_rating_distribution(df: pd.DataFrame, top_n=20):
    if "rating" not in df.columns:
        print("No rating column present")
        return
    counts = df["rating"].value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=counts.values, y=counts.index, ax=ax)
    ax.set_title("Content Ratings Distribution")
    ax.set_xlabel("Count")
    ax.set_ylabel("")
    plt.tight_layout()
    path = os.path.join(SCRIPT_DIR, "plots", "rating_distribution.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved {path}")


def duration_insights(df: pd.DataFrame):
    movies = df[df["type"].str.lower() == "movie"] if "type" in df.columns else df
    shows = df[df["type"].str.lower() == "tv show"] if "type" in df.columns else pd.DataFrame()

    # Movies - minutes distribution
    if not movies.empty and "duration_parsed" in movies.columns:
        m = movies["duration_parsed"].dropna()
        if not m.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(m, bins=30, kde=False, ax=ax)
            ax.set_title("Distribution of Movie Durations (minutes)")
            ax.set_xlabel("Minutes")
            plt.tight_layout()
            path = os.path.join(SCRIPT_DIR, "plots", "movie_duration_distribution.png")
            fig.savefig(path)
            plt.close(fig)
            print(f"Saved {path}")

    # Shows - seasons distribution
    if not shows.empty and "duration_parsed" in shows.columns:
        s = shows["duration_parsed"].dropna()
        if not s.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.countplot(x=s, ax=ax)
            ax.set_title("Number of Seasons for TV Shows")
            ax.set_xlabel("Seasons")
            plt.tight_layout()
            path = os.path.join(SCRIPT_DIR, "plots", "show_seasons_count.png")
            fig.savefig(path)
            plt.close(fig)
            print(f"Saved {path}")


def top_directors_actors(df: pd.DataFrame, top_n=10):
    # Directors
    directors = df["director"].dropna().astype(str)
    directors = directors[directors != "Unknown"]
    if not directors.empty:
        dir_counts = directors.value_counts().head(top_n)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=dir_counts.values, y=dir_counts.index, ax=ax)
        ax.set_title(f"Top {top_n} Directors by Number of Titles")
        ax.set_xlabel("Number of Titles")
        plt.tight_layout()
        path = os.path.join(SCRIPT_DIR, "plots", "top_directors.png")
        fig.savefig(path)
        plt.close(fig)
        print(f"Saved {path}")

    # Actors: explode cast
    if "cast" in df.columns:
        casts = df["cast"].dropna().astype(str)
        actor_counter = Counter()
        for c in casts:
            for actor in [a.strip() for a in c.split(",")][:5]:  # only first 5 to avoid extremely long lists
                if actor:
                    actor_counter[actor] += 1
        top_actors = actor_counter.most_common(top_n)
        if top_actors:
            actors, counts = zip(*top_actors)
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=list(counts), y=list(actors), ax=ax)
            ax.set_title(f"Top {top_n} Actors/Actresses by Appearances (first 5 listed)")
            ax.set_xlabel("Appearances")
            plt.tight_layout()
            path = os.path.join(SCRIPT_DIR, "plots", "top_actors.png")
            fig.savefig(path)
            plt.close(fig)
            print(f"Saved {path}")


def save_summary(df: pd.DataFrame):
    summary = {}
    summary["total_titles"] = len(df)
    if "type" in df.columns:
        summary.update(df["type"].value_counts().to_dict())
    if "year_added" in df.columns:
        summary["earliest_year_added"] = int(df["year_added"].dropna().min()) if not df["year_added"].dropna().empty else np.nan
        summary["latest_year_added"] = int(df["year_added"].dropna().max()) if not df["year_added"].dropna().empty else np.nan

    # top country
    summary["top_country"] = df["primary_country"].value_counts().idxmax() if not df["primary_country"].empty else "Unknown"

    summary_df = pd.DataFrame(list(summary.items()), columns=["metric", "value"]) 
    out_path = os.path.join(SCRIPT_DIR, "output", "summary_stats.csv")
    summary_df.to_csv(out_path, index=False)
    print(f"Saved summary to {out_path}")


def main(args):
    ensure_dirs()
    df = read_data(args.csv)
    df = clean_data(df)

    # Run analyses and save plots
    plot_movies_vs_tv(df)
    plot_top_genres(df, top_n=args.top_genres)
    plot_yearly_trend(df)
    plot_top_countries(df, top_n=args.top_countries)
    plot_rating_distribution(df)
    duration_insights(df)
    top_directors_actors(df, top_n=args.top_people)
    save_summary(df)

    print("All done. Plots are in the ./plots directory and summary in ./output.")

if __name__ == "__main__":
    class Args:
        csv = r"C:\Users\pc\Downloads\archive (1)\netflix_titles.csv"   # <-- Your CSV path
        top_genres = 12
        top_countries = 10
        top_people = 10

    args = Args()
    main(args)


  
