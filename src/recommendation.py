from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils import parse_json_safely
from persona import llm

# 영화 추천 템플릿
recommendation_template = """
당신은 사용자의 영화 취향을 정확히 이해하고 그에 맞춘 영화를 추천하는 영화 추천 전문가입니다. 사용자의 페르소나와 추가 정보, 영화 후보 리스트를 바탕으로 각 영화가 사용자에게 어떻게 맞는지 분석하여 movie_candidates에서 반드시 4편을 선택하고, movie_candidates에 없는 영화 2편을 선택하여 총 6편의 영화를 추천해 주세요.


페르소나: {persona}
영화 후보 리스트: {movie_candidates}
이미 시청한 영화 기록: {watched_movies}
추가 정보: {user_input}

## 최종 추천 영화 선정 작업:
1. movie_candidates에서 반드시 4편을 선택하고, movie_candidates에 없는 영화 2편을 추가하여 총 6편을 추천하세요. 추가 추천 영화는 반드시 실제로 존재하는 영화여야 하며, 페르소나의 취향을 벗어나 새로운 경험을 제공할 수 있는 작품으로 선정하세요.
2. movie_candidates애 적절한 영화가 없더라도 반드시 4편의 영화를 movie_candidates에서 선택해라.
3. 추천 시 다음 사항을 고려하세요:
   • 사용자의 취향과 관심사에 맞는 영화
   • 다양한 장르와 스타일을 포함
   • 영화 감상 목적이나 감정 상태에 어울리는 영화
   • 사용자가 선호하는 언어나 문화적 배경
   • user_input에 대한 추가 정보를 반영
4. 각 영화에 대한 추천 이유를 자세하게 설명하고, 사용자의 페르소나와 어떻게 연결되는지 언급하세요.
결과를 반드시 다음 JSON 형식으로만 출력하고 괄호를 제대로 열고 닫았는지 확인해줘:
{{
    "recommendations": 
    {{  "title": "영화 제목",
        "reason": "추천 이유"   }},
    ...
}}
        
"""

recommendation_prompt = PromptTemplate(
    input_variables=[
        "persona",
        "movie_candidates",
        "watched_movies",
        "user_input",
    ],
    template=recommendation_template
)

recommendation_chain = LLMChain(llm=llm, prompt=recommendation_prompt)

from datetime import datetime

def recommend_movies(request):
    try:
        # 현재 시간을 문자열로 변환
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        recommendations = recommendation_chain.run(
            persona=request.persona,
            movie_candidates=", ".join(request.movie_candidates),
            watched_movies=", ".join(request.watched_movies),
            user_input=request.user_input if request.user_input else "정보 없음",
            request_time=current_time
        )
        print(f"Raw recommendation output: {recommendations}")
        return parse_json_safely(recommendations)
    except Exception as e:
        raise ValueError(f"Error recommending movies: {e}")