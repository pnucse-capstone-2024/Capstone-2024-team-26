from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils import parse_json_safely
from persona import llm

# 사용자 정보 정리 템플릿
organize_template = """
사용자가 제공한 다양한 정보를 깔끔하게 정리하세요. 사용자가 말한 직업, 취미, 성격, 감정 상태, 선호하는 영화 및 감독, 영화를 보는 목적 등 여러 요소를 잘 요약하고, 의미가 불분명한 문장은 명확하게 다듬어 주세요.

사용자 입력: {user_input}

정리된 결과물은 다음과 같은 방식으로 출력하세요:
- 사용자의 직업과 취미를 간결하게 설명
- 성격이나 성향을 반영하는 특징을 요약
- 최근에 시청한 영화나 선호하는 영화 감독/배우를 명확하게 기술
- 현재의 감정 상태와 영화를 보고자 하는 이유를 명확하게 서술
- 형식이 불분명하거나 모호한 문장은 더 명확하게 표현

불분명한 정보는 적절히 다듬어서 전체적으로 자연스럽고 읽기 쉬운 문장으로 정리하세요.
"""

organize_prompt = PromptTemplate(
    input_variables=["user_input"],
    template=organize_template
)

organize_chain = LLMChain(llm=llm, prompt=organize_prompt)

def organize_user_info(user_input):
    try:
        organized_info = organize_chain.run(user_input=user_input)
        return parse_json_safely(organized_info)
    except Exception as e:
        raise ValueError(f"Error organizing user info: {e}")