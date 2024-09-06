import numpy as np
import pandas as pd
import ast  # To convert string to list
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import PorterStemmer

# Initialize the Porter Stemmer
ps = PorterStemmer()

# Helper Methods

def transform(obj):
    """
    Transforms a string representation of a list of dictionaries into a list of names.
    
    Args:
        obj (str): String representation of a list of dictionaries.
    
    Returns:
        list: List of names extracted from the dictionaries.
    """
    names = []
    for item in ast.literal_eval(obj):
        names.append(item['name'])
    return names

def transform_II(obj):
    """
    Transforms a string representation of a list of dictionaries into a list of the first 3 names.
    
    Args:
        obj (str): String representation of a list of dictionaries.
    
    Returns:
        list: List of the first 3 names extracted from the dictionaries.
    """
    names = []
    for index, item in enumerate(ast.literal_eval(obj)):
        if index < 3:
            names.append(item['name'])
        else:
            break
    return names

def transform_III(obj):
    """
    Transforms a string representation of a list of dictionaries into a list with only the director's name.
    
    Args:
        obj (str): String representation of a list of dictionaries.
    
    Returns:
        list: List containing the name of the director, if found.
    """
    names = []
    for item in ast.literal_eval(obj):
        if item['job'] == "Director":
            names.append(item['name'])
            break
    return names

def transform_stem(text):
    """
    Applies stemming to each word in the input text.
    
    Args:
        text (str): Input text to be stemmed.
    
    Returns:
        str: Stemmed text.
    """
    words = text.split()
    stemmed_words = [ps.stem(word) for word in words]
    return " ".join(stemmed_words)

# Load datasets
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.read_csv('tmdb_5000_movies.csv')

# Merge datasets on 'title'
movies = movies.merge(credits, on='title')

# Keep relevant datapoints
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

# Apply transformations
movies['genres'] = movies['genres'].apply(transform)
movies['keywords'] = movies['keywords'].apply(transform)
movies['cast'] = movies['cast'].apply(transform_II)
movies['crew'] = movies['crew'].apply(transform_III)

# Process 'overview', 'genres', 'keywords', 'cast', and 'crew'
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# Combine all text features into 'tags'
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Create new DataFrame with 'movie_id', 'title', and 'tags'
new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Apply stemming to tags
new_df['tags'] = new_df['tags'].apply(transform_stem)

# Compute similarity matrix
similarity = cosine_similarity(vectors)

def recommend(movie_title):
    """
    Recommends movies similar to the given movie title.
    
    Args:
        movie_title (str): The title of the movie for which recommendations are to be made.
    
    Returns:
        list: List of indices of recommended movies.
    """
    movie_index = new_df[new_df['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    
    # Get the indices of the top 5 most similar movies
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    return similar_movies
