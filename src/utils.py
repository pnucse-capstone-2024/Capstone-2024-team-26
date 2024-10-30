import json
import re


def preprocess_json(text):
    # 문자열 내의 \' 문자 제거
    text = text.replace("\\'", "")

    # JSON 객체 추출
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        json_str = match.group(0)
        # \n 문자 제거
        json_str = json_str.replace("\\n", "")
        # 모든 공백 문자 제거
        json_str = re.sub(r'\s+', ' ', json_str)
        return json_str
    return text


def parse_json_safely(text):
    try:
        preprocessed_text = preprocess_json(text)
        print(preprocessed_text)  # 디버깅용 출력
        return json.loads(preprocessed_text)  # JSON 파싱
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        return {
            "error": "JSON 파싱 실패",
            "message": str(e),
            "raw_text": text
        }