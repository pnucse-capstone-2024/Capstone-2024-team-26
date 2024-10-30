from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils import parse_json_safely
from langchain.llms import Ollama

llm = Ollama(model="EEVE-KR:latest")
# 페르소나 생성 템플릿
persona_template = """
당신은 영화 추천을 위한 사용자 페르소나를 만드는 전문가입니다. 주어진 정보를 바탕으로 JSON 형식의 상세한 페르소나를 생성해주세요.

사용자 정보:
- 나이: {age}
- 성별: {gender}
- 직업: {job}
- 유저가 제공한 추가 정보: {user_input}

제공된 정보 중 일부가 비어있을 수 있습니다. 빈 값이 있으면 해당 정보를 무시하거나 그에 맞는 추론을 해주세요.

### 페르소나 생성 작업:
1. 명시된 정보 (나이, 직업 등), 추론 정보 (시청 패턴, 선호도), 불확실 정보 (검증 필요사항)
2. 작성 규칙:
    - 명시 정보로 기본 프로필 작성
    - 추론 시 근거 제시
    - 불확실한 내용은 범위로 표현
3. 필수 요소
    - 기본 정보 (인구통계학적 특성)
    - 시청 습관 (시간대, 빈도)
    - 선호도 (장르, 요소)
    - 제약사항 (기피 요소)
4. 주의사항
    - 극단적 성향 기술 금지
    - 모든 추론에 근거 필요
    - 정보 부족 시 통계 참고
    - 변화 가능성 고려

페르소나는 200자 이내로 작성하여 구체적이고 활용 가능한 정보를 제공하세요.
띄어쓰기 줄바꿈은 하지마라.
결과는 다음 JSON 형식으로 제공해주세요:

{{
  "persona": "페르소나에 대한 설명"
}}

상세하고 일관된 페르소나를 생성해주세요.
"""

persona_prompt = PromptTemplate(
    input_variables=[
        "age",
        "gender",
        "job",
        "user_input",
    ],
    template=persona_template
)

persona_chain = LLMChain(llm=llm, prompt=persona_prompt)

def generate_persona(user_info):
    try:
        persona = persona_chain.run(
            age=user_info.age if user_info.age else "정보 없음",
            gender=user_info.gender if user_info.gender else "정보 없음",
            job=user_info.job if user_info.job else "정보 없음",
            user_input=user_info.user_input if user_info.user_input else "정보 없음"
        )
        print(f"Raw persona output: {persona}")
        return parse_json_safely(persona)
    except Exception as e:
        raise ValueError(f"Error generating persona: {e}")

    
# 페르소나 생성 끝
    
# 페르소나 업데이트 템플릿
update_persona_template = """
당신은 영화 추천을 위한 사용자 페르소나를 업데이트하는 전문가입니다. 아래의 기존 페르소나와 새로운 정보를 바탕으로 업데이트된 페르소나를 생성해주세요.

기존 페르소나:
{existing_persona}

새로운 정보:
{user_input}

### 페르소나 업데이트 작업:
1. 새로운 정보에 따라 기존 페르소나의 성격, 취미, 영화 선호도를 업데이트하세요.
2. user_input에 추가된 정보가 기존 페르소나에 미치는 영향을 고려하여 적절히 조정하거나 추가하세요.
3. 업데이트된 페르소나 설명은 JSON 형식으로 제공되어야 하며, "updated_persona": "업데이트된 페르소나"의 형식으로 반환해야 합니다.

결과는 JSON 형식으로 반환해주세요:
{{
    "updated_persona": "생성된 업데이트된 페르소나"
}}
"""

update_persona_prompt = PromptTemplate(
    input_variables=["existing_persona", "user_input"],
    template=update_persona_template
)

update_persona_chain = LLMChain(llm=llm, prompt=update_persona_prompt)

# 페르소나 업데이트
def update_persona(existing_persona, user_input):
    try:
        updated_persona = update_persona_chain.run(
            existing_persona=existing_persona,
            user_input=user_input
        )
        print(f"Raw updated persona output: {updated_persona}")
        return parse_json_safely(updated_persona)
    except Exception as e:
        raise ValueError(f"Error updating persona: {e}")