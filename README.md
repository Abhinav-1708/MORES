**Movie Recommendation System**

This project is a movie recommendation system built using Streamlit. The system recommends movies similar to a selected movie using cosine similarity and vectorization techniques. Data is fetched from [The Movie Database (TMDB) API](https://www.themoviedb.org/).

**How It Works**

- **Data Processing**:
    - The project uses movie data from TMDB. The data is processed by combining features such as genres, keywords, cast, and crew into a single tags column.
    - Text data is vectorized using CountVectorizer, and stemming is applied to improve similarity calculations.
    - Cosine similarity is used to recommend similar movies based on the selected movie.
- **Movie Poster Fetching**:
    - Posters are fetched from TMDB using an API key.

**Requirements**

Ensure you have the following Python packages installed:

```
nltk==3.9.1
numpy==2.1.1
pandas==2.2.2
requests==2.32.3
scikit_learn==1.5.1
streamlit==1.38.0
```

You can install the required packages using

```
pip install nltk==3.9.1 numpy==2.1.1 pandas==2.2.2 requests==2.32.3 scikit_learn==1.5.1 streamlit==1.38.0
```

**Setup**

1. **Clone the repository** or download the project files.
2. **Create a configuration file** named config.json in the project directory with your TMDB API key:

```
{

"TMDB_API_KEY": "your_api_key_here"

}
```

1. **Prepare the data**: Make sure you have the CSV files tmdb_5000_credits.csv and tmdb_5000_movies.csv in the project directory.
2. **Run the Streamlit app**:

```
streamlit run app.py
```

Replace app.py with the name of your Streamlit application file if it's different.

**Usage**

- Open the Streamlit app in your browser.
- Select a movie from the dropdown list.
- Click the "Recommend" button to get a list of similar movies along with their posters.