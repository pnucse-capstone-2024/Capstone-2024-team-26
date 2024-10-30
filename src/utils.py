import json
import re

def preprocess_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        json_str = match.group(0)
        json_str = re.sub(r'\s+', ' ', json_str)
        return json_str
    return text

def parse_json_safely(text):
    try:
        preprocessed_text = preprocess_json(text)
        print(preprocessed_text)
        return json.loads(preprocessed_text)
    except json.JSONDecodeError as e:
        return {
            "error": "JSON 파싱 실패",
            "message": str(e),
            "raw_text": text
        }