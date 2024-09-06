import streamlit as st
import numpy as np
import pandas as pd
import pickle
import requests
import json

def load_config():
    """
    Loads configuration from a JSON file.
    
    Returns:
        dict: Configuration dictionary with API key.
    """
    with open('config.json', 'r') as file:
        return json.load(file)

# Load API key from configuration
config = load_config()
api_key = config['TMDB_API_KEY']

def fetch_poster(movie_id):
    """
    Fetches the poster URL for a given movie ID from The Movie Database API.
    
    Args:
        movie_id (int): The ID of the movie.
    
    Returns:
        str: URL of the movie poster.
    """
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

def recommend(movie_title):
    """
    Recommends movies similar to the selected movie.
    
    Args:
        movie_title (str): The title of the selected movie.
    
    Returns:
        tuple: Two lists containing recommended movie titles and their corresponding poster URLs.
    """
    # Find the index of the selected movie in the movies list
    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    
    # Get the indices of the top 5 most similar movies
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_titles = []
    recommended_posters = []
    
    for i in similar_movies:
        movie_id = movies_df.iloc[i[0]].movie_id
        # Fetch movie poster from API
        recommended_titles.append(movies_df.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_titles, recommended_posters

# Load precomputed data
movies_df = pickle.load(open("movies.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# List of movie titles for the dropdown
movie_titles = movies_df['title'].values

# Streamlit app layout
st.title("Movie Recommendation System")

# Movie selection dropdown
selected_movie_title = st.selectbox("Select a Movie", movie_titles)

if st.button("Recommend"):
    titles, posters = recommend(selected_movie_title)
    
    # Display recommended movies and their posters
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(titles[0])
        st.image(posters[0])
    with col2:
        st.text(titles[1])
        st.image(posters[1])
    with col3:
        st.text(titles[2])
        st.image(posters[2])
    with col4:
        st.text(titles[3])
        st.image(posters[3])
    with col5:
        st.text(titles[4])
        st.image(posters[4])
