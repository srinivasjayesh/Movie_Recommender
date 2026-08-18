import streamlit as st
import pickle
import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
import time




@st.cache_data(show_spinner="Getting your next watch...")
def fetch_posters(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }

    for attempt in range(4):
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                poster_path = data.get("poster_path")

                if poster_path:
                    return "https://image.tmdb.org/t/p/w500/" + poster_path.lstrip("/")

                return "https://via.placeholder.com/500x750?text=No+Poster"

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {movie_id}: {e}")
            time.sleep(1 + attempt)

    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]]["movie_id"]

        recommended_movies.append(
            movies.iloc[i[0]]["title"]
        )

        recommended_posters.append(
            fetch_posters(movie_id)
        )

    return recommended_movies, recommended_posters


similarity = pickle.load(
    open("similarity.pkl", "rb")
)

movies_dict = pickle.load(
    open("movie_dict.pkl", "rb")
)

movies = pd.DataFrame(movies_dict)


st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    "Select Movie",
    movies["title"].values
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

    with col2:
        st.image(posters[1])
        st.caption(names[1])

    with col3:
        st.image(posters[2])
        st.caption(names[2])

    with col4:
        st.image(posters[3])
        st.caption(names[3])

    with col5:
        st.image(posters[4])
        st.caption(names[4])