import pandas as pd
import streamlit as st
import pickle
import requests  # for hitting API

# ✅ keep API key in a variable (looks cleaner)
API_KEY = "8511be0bf7fdbabf62ca2fbc5f7bb031"


def fetch_poster(movie_id):
    """
    Fetch poster URL for a given TMDB movie_id.
    Tries TMDB API; if it fails (timeout, network, etc.), returns a placeholder image.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    try:
        # timeout=5 so it doesn’t hang forever
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")
        if not poster_path:
            # No poster for this movie -> show a neutral placeholder
            return "https://via.placeholder.com/300x450?text=No+Poster"

        return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception as e:
        # This prevents Streamlit from crashing if TMDB is unreachable
        print("Error fetching poster for movie_id", movie_id, ":", e)
        return "https://via.placeholder.com/300x450?text=Error"



def recommend(movie):
    """
    For a given movie title, find similar movies using the precomputed similarity matrix.
    Returns:
      - list of recommended movie titles
      - list of poster image URLs for those movies
    """
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]  # skip the first one (it’s the same movie)

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# ✅ load preprocessed movie data and similarity matrix
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# ✅ streamlit UI
st.title("Movie Recommendation System (Content-Based)")

selected_movie_name = st.selectbox(
    "Select a movie, I’ll recommend similar ones:",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
