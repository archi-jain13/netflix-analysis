# Netflix Movies & TV Shows - Data Analysis Project

A Python-based data analysis project that explores and visualizes Netflix's content catalog using exploratory data analysis (EDA) techniques.

## 📊 Overview

This project analyzes Netflix's movies and TV shows dataset to uncover insights about:
- Content distribution (Movies vs TV Shows)
- Genre popularity trends
- Content addition patterns over time
- Geographic distribution of content production
- Rating distributions
- Duration analysis (movie lengths and TV show seasons)
- Top directors and actors/actresses

## 📁 Project Structure

```
DA project/
├── da.py                      # Main analysis script
├── plots/                     # Generated visualization plots (PNG files)
│   ├── movies_vs_tv.png
│   ├── top_genres.png
│   ├── content_added_per_year.png
│   ├── top_countries.png
│   ├── rating_distribution.png
│   ├── movie_duration_distribution.png
│   ├── show_seasons_count.png
│   ├── top_directors.png
│   └── top_actors.png
└── output/
    └── summary_stats.csv      # Summary statistics
```

## 🛠️ Requirements

- Python 3.7+
- Required libraries:
  ```
  pandas
  matplotlib
  seaborn
  numpy
  ```

## 📦 Installation

Install the required dependencies:

```bash
pip install pandas matplotlib seaborn numpy
```

## 🚀 Usage

1. Prepare your Netflix dataset (CSV format with columns like `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, etc.)

2. Update the CSV path in `da.py` (line 297):
   ```python
   csv = r"path/to/your/netflix_titles.csv"
   ```

3. Run the analysis:
   ```bash
   python da.py
   ```

4. View the generated plots in the `./plots/` directory and summary statistics in `./output/summary_stats.csv`

## 📈 Generated Visualizations

The script automatically generates the following plots:

1. **Movies vs TV Shows** - Distribution of content types
2. **Top Genres** - Most popular genres/categories
3. **Content Added Per Year** - Yearly trend of content additions
4. **Top Countries** - Leading content-producing countries
5. **Rating Distribution** - Content rating breakdown
6. **Movie Duration Distribution** - Histogram of movie lengths
7. **TV Show Seasons** - Distribution of number of seasons
8. **Top Directors** - Most prolific directors on Netflix
9. **Top Actors** - Most frequently appearing actors/actresses

## 📊 Output

- **Plots**: High-quality PNG files saved in `./plots/` directory
- **Summary Statistics**: Key metrics exported to `./output/summary_stats.csv`

## 🔧 Customization

You can customize the analysis parameters in the `Args` class:

```python
class Args:
    csv = r"path/to/netflix_titles.csv"
    top_genres = 12        # Number of top genres to display
    top_countries = 10     # Number of top countries to display
    top_people = 10        # Number of top directors/actors to display
```

## 📝 Data Processing

The script includes comprehensive data cleaning:
- Standardizes column names
- Parses dates and extracts year information
- Handles missing values
- Normalizes content types
- Splits and processes genre lists
- Parses duration information (minutes for movies, seasons for TV shows)
- Extracts primary country from multi-country listings

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

Dataset source: Netflix Movies and TV Shows dataset (commonly available on Kaggle and other data repositories)

---

**Note**: This project is designed for educational and analytical purposes to explore data analysis techniques using Python.
