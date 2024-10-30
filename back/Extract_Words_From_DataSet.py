import pandas as pd
import ast
import json

# CSV 파일 로드
data = pd.read_csv('../Dataset/original_data.csv')


def extract_unique_items(column):
    unique_items = set()
    for item in column:
        try:
            # 문자열을 리스트로 변환
            item_list = ast.literal_eval(item)
            # 리스트의 각 항목에서 이름만 추출
            for sub_item in item_list:
                if isinstance(sub_item, dict) and 'name' in sub_item:
                    unique_items.add(sub_item['name'])
                elif isinstance(sub_item, str):
                    unique_items.add(sub_item)
        except:
            pass
    return sorted(list(unique_items))


# genres, credits(actors), keywords에서 고유한 항목 추출
unique_genres = extract_unique_items(data['genres'])
unique_actors = extract_unique_items(data['credits'])
unique_keywords = extract_unique_items(data['keywords'])

# 결과를 JSON 파일로 저장
with open('unique_genres.json', 'w', encoding='utf-8') as f:
    json.dump(unique_genres, f, ensure_ascii=False, indent=4)

with open('unique_actors.json', 'w', encoding='utf-8') as f:
    json.dump(unique_actors, f, ensure_ascii=False, indent=4)

with open('unique_keywords.json', 'w', encoding='utf-8') as f:
    json.dump(unique_keywords, f, ensure_ascii=False, indent=4)

print("고유한 장르 수:", len(unique_genres))
print("고유한 배우 수:", len(unique_actors))
print("고유한 키워드 수:", len(unique_keywords))