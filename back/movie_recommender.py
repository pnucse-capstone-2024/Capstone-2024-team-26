
import numpy as np
from scipy.sparse import load_npz, csr_matrix
import pandas as pd
import joblib

# 데이터 로딩
m_data = pd.read_csv('./Dataset/original_data.csv')
encoded_features = load_npz('./Dataset/encoded_features.npz')
mlb_genre = joblib.load('./Dataset/mlb_genre.joblib')
mlb_actor = joblib.load('./Dataset/mlb_actor.joblib')


def get_recommendations(genres, directors, top_n=10):
    genre_vector = mlb_genre.transform([genres])
    director_vector = mlb_actor.transform([directors]) 

    input_vector = csr_matrix((1, encoded_features.shape[1]))
    input_vector[:, :genre_vector.shape[1]] = genre_vector
    input_vector[:, genre_vector.shape[1]:genre_vector.shape[1] + director_vector.shape[1]] = director_vector

    similarities = encoded_features.dot(input_vector.T).toarray().flatten()

    top_indices = np.argsort(similarities)[-top_n:][::-1]

    return top_indices
