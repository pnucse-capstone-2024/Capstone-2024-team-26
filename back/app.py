from flask import Flask, request, jsonify
import requests
import mysql.connector
from flask_cors import CORS
from movie_recommender import get_recommendations, m_data
import numpy as np
app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="125.184.62.136",
        user="new_user",
        password="new_password",
        database="movie_db"
    )


@app.route('/<string:name>/call_fastapi_persona', methods=['POST'])
def call_fastapi_persona(name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT age, gender, job, user_input, persona FROM user WHERE name = %s', (name,))
        user_row = cursor.fetchone()

        if not user_row:
            return jsonify({"error": "User not found"}), 404

        user_info = {
            "age": user_row["age"],
            "gender": user_row["gender"],
            "job": user_row["job"],
            "user_input": user_row["user_input"]
        }



        fastapi_url = "http://localhost:8000/generate_persona"
        request_data = user_info

        response = requests.post(fastapi_url, json=request_data)

        if response.status_code == 200:
            print(response.text)  # 결과값을 JSON 형태로 출력
        else:
            print(f"Error: {response.status_code}, {response.text}")

        # FastAPI 서버 요청이 실패한 경우 처리
        if response.status_code != 200:
            return jsonify({"error": "Failed to call FastAPI"}), response.status_code

        # 요청이 성공적으로 처리되었을 때 페르소나 업데이트
        cursor.execute("UPDATE user SET persona = %s WHERE name = %s", (response.json().get("persona"), name))
        print(response)
        conn.commit()

        # 요청이 성공적으로 처리되었음을 클라이언트에 알림
        return jsonify({"message": "Persona processed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # 데이터베이스 연결 자원 해제
        cursor.close()
        conn.close()



@app.route('/<string:name>/user_get_recommendations', methods=['GET'])
def user_get_recommendations(name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True,buffered=True)

        # 사용자 정보를 가져옵니다.
        cursor.execute(
            'SELECT persona, movie_candidates, watched_movies, user_input FROM user WHERE name = %s', (name,)
        )
        persona_row = cursor.fetchone()

        if persona_row is None:
            return jsonify({"error": "User not found"}), 404  # 사용자 정보가 없을 때

        movie_candidates = persona_row.get("movie_candidates", []).split(',')
        watched_movies = persona_row.get("watched_movies", []).split(',')
        if persona_row and persona_row["persona"]:
            # 영화 추천을 위한 데이터 구성
            movie_request_data = {
                "persona": persona_row["persona"],
                "movie_candidates": movie_candidates,
                "watched_movies": watched_movies,
                "user_input": persona_row.get("user_input", "")
            }


            # FastAPI 서버에 추천 요청 전송
            fastapi_url = "http://localhost:8000/recommend_movies"

            response = requests.post(fastapi_url, json=movie_request_data)
            print(response)
            response_data = response.json()["recommendations"]


            # 각 영화에 대한 genres와 credits 정보 추가
            for movie in response_data:
                title = movie.get("title")

                # 영화 제목으로 장르와 출연 배우 정보 가져오기
                cursor.execute(
                    'SELECT genres, credits FROM movies WHERE title = %s', (title,)
                )
                movie_info = cursor.fetchone()
                
                if movie_info:
                    movie["genres"] = movie_info["genres"]
                    movie["credits"] = movie_info["credits"]

            return jsonify(response_data), response.status_code

        return jsonify({"error": "No persona available for the user."}), 400  # persona가 없는 경우

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# 사용자 입력 데이터를 정리하는 FastAPI 요청을 보냅니다.
@app.route('/organize_user_info', methods=['POST'])
def organize_user_info():
    user_input = request.json.get("user_input", "")
    fastapi_url = "http://localhost:8000/organize_input"
    
    response = requests.post(fastapi_url, json={"user_input": user_input})

    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({"error": "사용자 정보 정리 실패"}), 500



# 검색 쿼리에 따라 영화 또는 장르 및 배우를 검색합니다.
@app.route('/api/search', methods=['GET'])
def search_items():
    query = request.args.get('query')
    search_type = request.args.get('type')
    
    if not query or not search_type:
        return jsonify({"error": "Query and type parameters are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search_type == 'movies':
        cursor.execute("SELECT title FROM movies WHERE title LIKE %s LIMIT 10", ('%' + query + '%',))
    elif search_type == 'genres':
        cursor.execute("SELECT name AS genre FROM genres WHERE name LIKE %s LIMIT 10", ('%' + query + '%',))
    elif search_type == 'actors':
        cursor.execute("SELECT name AS actors FROM actors WHERE name LIKE %s LIMIT 10", ('%' + query + '%',))

    else:
        return jsonify({"error": "Invalid type parameter"}), 400

    results = cursor.fetchall()
    print(results)
    conn.close()
    
    return jsonify(results)

#사용자 입력 데이터를 업데이트합니다.
@app.route('/api/users/<string:name>/update_user_input', methods=['PUT'])
def update_user_input(name):
    data = request.json
    user_input = data.get('user_input')

    if not user_input:
        return jsonify({"error": "user_input is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        update_query = "UPDATE user SET user_input = %s WHERE name = %s"
        cursor.execute(update_query, (user_input, name))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User input updated successfully!"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": "Database error occurred"}), 500

    finally:
        cursor.close()
        conn.close()
        
# 사용자가 시청한 영화 목록을 조회합니다.    
@app.route('/api/users/<string:name>/get_watched_movies', methods=['GET'])
def get_watched_movies(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = 'SELECT watched_movies FROM user WHERE name = %s'
    cursor.execute(select_query, (name,))
    
    result = cursor.fetchone()

    conn.close()

    if result is None:
        return jsonify({'error': 'User not found'}), 404

    watched_movies = result[0] if result[0] else ''

    watched_movies_list = watched_movies.split(',') if watched_movies else []

    return jsonify({'watched_movies': watched_movies_list}), 200

# 사용자의 정보(영화, 배우, 장르)를 업데이트합니다.
@app.route('/api/users/<string:name>/add_item', methods=['PUT'])
def add_item(name):
    item = request.json.get('item')
    item_type = request.json.get('type') 
    if not item or not item_type:
        return jsonify({'error': 'Item and type are required'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()

    field_map = {
        'movie': 'watched_movies',
        'actor': 'directors',
        'genre': 'genres'
    }

    if item_type not in field_map:
        return jsonify({'error': 'Invalid item type'}), 400

    field = field_map[item_type]

    select_query = f'SELECT {field} FROM user WHERE name = %s'
    cursor.execute(select_query, (name,))
    result = cursor.fetchone()

    if result is None:
        return jsonify({'error': 'User not found'}), 404

    existing_items = result[0] if result[0] else ''

    updated_items = f"{existing_items},{item}" if existing_items else item
    update_query = f'UPDATE user SET {field} = %s WHERE name = %s'
    cursor.execute(update_query, (updated_items, name))
    conn.commit()

    conn.close()
    return jsonify({'message': f'{item_type.capitalize()} added successfully'}), 200

@app.route('/api/users/<string:name>/fetch_recommendations', methods=['GET'])
def fetch_recommendations(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT genres, directors FROM user WHERE name = %s", (name,))
    user_info = cursor.fetchone()

    if user_info is None:
        return jsonify({'error': 'User not found'}), 404

    genres = user_info['genres'].split(',') if user_info['genres'] else []
    directors = user_info['directors'].split(',') if user_info['directors'] else []

    recommendations = get_recommendations(genres, directors)

    # recommendations가 배열인 경우 길이를 확인합니다.
    if isinstance(recommendations, (list, np.ndarray)) and len(recommendations) == 0:
        return jsonify({'message': 'No recommendations available'}), 404  # 추천이 없을 경우 처리

    recommendation_details = [
        {
            "title": m_data.iloc[idx]['title']
        }
        for idx in recommendations if idx < len(m_data)
    ]

    movie_candidates_str = ','.join([movie['title'] for movie in recommendation_details])
    cursor.execute("UPDATE user SET movie_candidates = %s WHERE name = %s", (movie_candidates_str, name))
    conn.commit()

    return '', 204  # 추천 업데이트 완료 후 204 반환



# 특정 영화의 상세 정보를 반환합니다.
@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM movies WHERE movie_id = %s', (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    return jsonify(movie)

# 사용자가 영화에 평가를 추가합니다.
@app.route('/api/users/<string:name>/ratings', methods=['POST'])
def add_rating(name):
    movie_id = request.json.get('movie_id')
    rating = request.json.get('rating')
    conn = get_db_connection()
    cursor = conn.cursor()
    conn.commit()
    conn.close()
    return jsonify({"message": "Rating submitted"}), 201

# 사용자의 프로필 정보를 추가하거나 업데이트합니다.
@app.route('/api/users/<string:name>/profile', methods=['PUT'])
def update_profile(name):
    age = request.json.get('age')
    gender = request.json.get('gender')
    job = request.json.get('job')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM user WHERE name = %s', (name,))
    exists = cursor.fetchone()[0] > 0

    if exists:
        cursor.execute('UPDATE user SET age = %s, gender = %s, job = %s WHERE name = %s', (age, gender, job, name)) 
        conn.commit()
    else:
        cursor.execute('INSERT INTO user (name, age, gender, job) VALUES (%s, %s, %s, %s)', (name, age, gender, job))
        conn.commit()

    conn.close()
    return jsonify({}), 200

@app.route('/api/items/exists', methods=['GET'])
def item_exists():
    item_type = request.args.get('type')
    item_value = request.args.get('value')
    
    if not item_type or not item_value:
        return jsonify({"error": "Type and value parameters are required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    if item_type == 'movie':
        query = "SELECT COUNT(*) FROM movies WHERE LOWER(title) = LOWER(%s)"
    elif item_type == 'genre':
        query = "SELECT COUNT(*) FROM genres WHERE LOWER(name) = LOWER(%s)"
    elif item_type == 'actor':
        query = "SELECT COUNT(*) FROM actors WHERE LOWER(name) = LOWER(%s)"
    else:
        return jsonify({"error": "Invalid type parameter"}), 400

    cursor.execute(query, (item_value,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result[0] > 0:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 404





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
