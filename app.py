import pandas as pd
import streamlit as st
import pickle
# for hitting api we will use requests library
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                            '}?api_key=3bff838a120e02f0a6a0a0404b8afa14&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # for fetching poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System ')

selected_movie_name = st.selectbox(
    'suggest me a movie',
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













# import streamlit as st
# import pickle
#
# movies_list = pickle.load(open('movies.pkl', 'rb'))
# movies_list = movies_list['title'].values
#
# st.title('Movie Recommender System')
#
# selected_movie_name = st.selectable(
#     'Select a movie',
#     movies_list)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
#
# def recommend(movie):
#     movie_index = movies_list[selected_movie_name == movie].index[0]
#     distances = similarity[movie_index]
#     similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#     recommend_list = []
#     for i in similar_movies:
#         recommend_list.append(movies_list.iloc[i[0]].title)
#     return recommend_list
#
#
# if st.button('Recommend'):
#     recommendation = recommend(selected_movie_name)
#     st.write(selected_movie_name)
