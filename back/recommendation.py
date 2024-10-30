import numpy as np
from scipy.sparse import load_npz, csr_matrix
import pandas as pd
import joblib
from tqdm import tqdm

# print("사용 장치: CPU (numpy)")

# print("데이터 로딩 중...")
data = pd.read_csv('./Dataset/original_data.csv')
encoded_features = load_npz('./Dataset/encoded_features.npz')
mlb_genre = joblib.load('./Dataset/mlb_genre.joblib')
mlb_actor = joblib.load('./Dataset/mlb_actor.joblib')
# mlb_keyword = joblib.load('./mlb_keyword.joblib')
# print("데이터 로딩 완료")

# 데이터프레임 열 이름 확인
# print("데이터프레임 열:", data.columns)


def calculate_reliability_score(df):
    mean_rating = df['vote_average'].mean()
    min_votes = 10
    df['reliability_score'] = df.apply(lambda row: (row['vote_count'] / (row['vote_count'] + min_votes)) * row['vote_average'] + (min_votes / (row['vote_count'] + min_votes)) * mean_rating
                                        if row['vote_count'] > 0 else mean_rating, axis=1)
    return df

# 데이터 로딩 후 신뢰도 점수 계산
# print("신뢰도 점수 계산 중...")
data = calculate_reliability_score(data)
# print("신뢰도 점수 계산 완료")


# 장르 : 배우 : 평점값 : 평점수 : 신뢰도 점수 = 0.35 : 0.40 : 0.05 : 0.05 : 0.15 로 가중 설정
def get_recommendations(genres, actors, top_n=10, genre_weight=0.35, actor_weight=0.40,
                        rating_weight=0.05, popularity_weight=0.05, reliability_weight=0.15):
    # print("추천 계산 시작...")
    genre_vector = mlb_genre.transform([genres])
    actor_vector = mlb_actor.transform([actors])
    # keyword_vector = mlb_keyword.transform([keywords])

    weighted_vector = csr_matrix((1, encoded_features.shape[1]))

    genre_end = genre_vector.shape[1]
    actor_end = genre_end + actor_vector.shape[1]
    # keyword_end = actor_end + keyword_vector.shape[1]

    weighted_vector[:, :genre_end] = genre_vector * genre_weight
    weighted_vector[:, genre_end:actor_end] = actor_vector * actor_weight
    # weighted_vector[:, actor_end:keyword_end] = keyword_vector * keyword_weight

    similarities = encoded_features.dot(weighted_vector.T).toarray().flatten()

    normalized_ratings = (data['vote_average'] - data['vote_average'].min()) / (data['vote_average'].max() - data['vote_average'].min())
    normalized_popularity = (data['vote_count'] - data['vote_count'].min()) / (data['vote_count'].max() - data['vote_count'].min())
    normalized_reliability = (data['reliability_score'] - data['reliability_score'].min()) / (data['reliability_score'].max() - data['reliability_score'].min())

    combined_score = (similarities * (1 - rating_weight - popularity_weight - reliability_weight) +
                      normalized_ratings * rating_weight +
                      normalized_popularity * popularity_weight +
                      normalized_reliability * reliability_weight)

    # print("상위 추천 영화 선정 중...")
    top_indices = np.argsort(combined_score)[-top_n:][::-1]

    return top_indices


def recommend_movies(genres, actors, top_n=100):
    recommendation_titles = []

    # genres = input("선호하는 장르를 쉼표로 구분하여 입력해주세요 (예: Action, Adventure): ").split(',')
    # genres = [genre.strip().capitalize() for genre in genres]
    #
    # actors = input("선호하는 배우를 쉼표로 구분하여 입력해주세요 (예: Tom Cruise, Brad Pitt): ").split(',')
    # actors = [' '.join(word.capitalize() for word in actor.strip().split()) for actor in actors]
    #
    # keywords = input("선호하는 영화 키워드를 쉼표로 구분하여 입력해주세요 (예: superhero, time travel): ").split(',')
    # keywords = [keyword.strip().lower() for keyword in keywords]

    # print("추천 영화 검색 중...")
    recommendations = get_recommendations(genres, actors, top_n)

    # print("\n추천 영화:")
    for idx in recommendations:
        movie = data.iloc[idx]
        title = movie['title'] if 'title' in movie else "제목 없음"
        recommendation_titles.append(title)

        if 'release_date' in movie and pd.notna(movie['release_date']):
            pass
            # release_year = movie['release_date'][:4]
            # print(f"- {title} ({release_year})")
        else:
            pass
            # print(f"- {title}")

        if 'genres' in movie:
            genres = eval(movie['genres'])
            # print(f"  장르: {genres}")

        if 'credits' in movie:
            credits = eval(movie['credits'])
            # print(f"  출연: {credits}")

        # if 'keywords' in movie:
        #     keywords = eval(movie['keywords'])
            # print(f"  키워드: {keywords}")

        # print()

    # recommendation_titles = 리스트 형식
    # print(recommendation_titles)

    # recommendation_titles_str = Comma_Separated String 형식
    recommendation_titles_str = ""
    recommendation_titles_str = ", ".join(recommendation_titles)
    # print(recommendation_titles_str)
    # return recommendation_titles_str
    return recommendations
"""
if __name__ == "__main__":
    genres = input("선호하는 장르를 쉼표로 구분하여 입력해주세요 (예: Action, Adventure): ").split(',')
    genres = [genre.strip().capitalize() for genre in genres]

    actors = input("선호하는 배우를 쉼표로 구분하여 입력해주세요 (예: Tom Cruise, Brad Pitt): ").split(',')
    actors = [' '.join(word.capitalize() for word in actor.strip().split()) for actor in actors]

    # keywords = input("선호하는 영화 키워드를 쉼표로 구분하여 입력해주세요 (예: superhero, time travel): ").split(',')
    # keywords = [keyword.strip().lower() for keyword in keywords]

    # print(recommend_movies(genres, actors))
    # print(type(recommend_movies(genres, actors)))
"""