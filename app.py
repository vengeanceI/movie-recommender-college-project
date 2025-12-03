import pandas as pd
import streamlit as st
import pickle
import requests  # for API calls

# =======================
#  TMDB API CONFIG
# =======================
API_KEY = "8511be0bf7fdbabf62ca2fbc5f7bb031"  # your new key


def fetch_poster(movie_id):
    """
    Fetch poster URL from TMDB for a given movie_id.
    If the request fails (timeout / network / invalid id), return a placeholder image URL.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    try:
        # timeout so it doesn't hang forever
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")
        if not poster_path:
            # No poster found for this movie
            return "https://via.placeholder.com/300x450?text=No+Poster"

        return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception as e:
        # IMPORTANT: prevents the whole app from crashing
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/300x450?text=Error"


def recommend(movie):
    """
    Given a movie title, find the 5 most similar movies based on the similarity matrix.
    Returns:
      names  -> list of 5 movie titles
      posters -> list of 5 poster URLs
    """
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    # (index, similarity_score), sorted in descending similarity
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]  # skip index 0 (the same movie itself)

    recommended_movies = []
    recommended_movies_posters = []

    for i, _ in movies_list:
        movie_id = movies.iloc[i].movie_id
        recommended_movies.append(movies.iloc[i].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# =======================
#  LOAD DATA
# =======================
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# =======================
#  STREAMLIT UI
# =======================
st.title('Movie Recommendation System (Content-Based)')

selected_movie_name = st.selectbox(
    'Select a movie, I will recommend similar ones:',
    movies['title'].values
)

if st.button('Recommend'):
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
