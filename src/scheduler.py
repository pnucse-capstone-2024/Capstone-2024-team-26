# web server에서 주기적으로 요청하는 것으로 대체

'''import schedule
import time
from persona import generate_persona, llm
from recommendation import recommend_movies

def scheduled_update_and_recommend():
    user_id = 1  # 예시 사용자 ID
    user_data = get_user_data_from_db(user_id)
    existing_persona = get_persona_from_db(user_id)["persona"]
    movie_candidates = get_movie_candidates_from_db(user_id)

    updated_persona = generate_persona(user_data)
    recommend_movies({
        "persona": updated_persona,
        "movie_candidates": movie_candidates,
        "watched_movies": user_data["watched_movies"],
        "viewing_environment": "alone",
        "preferred_duration": "2 hours",
        "subtitle_preference": "yes",
        "rating_importance": "high",
        "recent_viewing_trend": "sci-fi",
        "current_mood": "relaxed"
    })

def run_scheduler():
    schedule.every(8).hours.do(scheduled_update_and_recommend)
    while True:
        schedule.run_pending()
        time.sleep(1)'''