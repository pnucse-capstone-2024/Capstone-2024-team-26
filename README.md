[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/NJK_cPkH)

<img src="https://github.com/user-attachments/assets/0b3b54b3-a293-4582-9367-c71cb20df3ba"  width="500" height="500"/>

---

# 1. 프로젝트 소개
## 1.1. 배경 및 필요성
### 대형 언어 모델과 추천 시스템 : 대화형 추천 시스템으로

2022년 OpenAI사의 대화형 인공지능 모델인 'ChatGPT'가 공개된 이래로 **대형 언어 모델**(**L**arge **L**anguage **M**odel, **LLM**) 분야는 끊임없이 발전을 거듭하고 있습니다.

* *더 빠른 **속도***

* *더 강력한 **성능***

* *더 저렴한 **비용***

위 세 키워드를 주 목표로 하여 발전해 온 대형 언어 모델들은 이제는 사람들의 일상 생활 속에서도 어렵지 않게 찾을 수 있게 되었습니다.


이러한 대형 언어 모델을 추천 시스템과 결합하는 시도가 과연 없었을까요?

정답은 '아니오'입니다.

추천 시스템과 대형 언어 모델을 결합,
기존 추천 시스템의 한계를 대형 언어 모델의 강력한 추론 능력을 활용하여 극복하고
사용자와의 동적인 대화를 통하여 더 세밀하고 더 개인화된 추천을 제공하는
**대화형 추천 시스템**(**C**onversational **R**ecommender **S**ystem, **CRS**)의 개념이 제시되었고, 현재까지도 활발한 연구가 이루어지고 있습니다.

### 대화형 추천 시스템 : 대형 언어 모델의 결합은 어떻게?
그렇다면, 대화형 추천 시스템을 구축하는 데에 있어서

* *대형 언어 모델은 어떠한 방식으로 **활용**되어야 할까요?*

* *또, 활용 방식이 정해졌다면 각 경우에 대해서 대형 언어 모델은 어떠한 **형식**의 출력을 해 주어야 할까요?*

위 질문들의 해답을 찾기 위한 연구들이 선행된 바가 있으나, 아쉽게도 명확하게 정립된 가이드라인의 정보는 부족한 것이 현 상황입니다.

이에 저희는 직접 대화형 추천 시스템을 구축, 서비스함으로써 위 질문들에 저희만의 해답을 내놓기 위하여 본 프로젝트를 진행하였습니다.

반갑습니다, 저희는 부산대학교 24년도 전기 졸업과제 팀 LLecommend입니다.


## 1.2. 목표 및 주요 내용

### 프로젝트 목표

#### 1. 추천 시스템 - 대형 언어 모델 연동 구조 정립 및 개발
기존의 연구 자료들을 기반으로 하여 추천 시스템과 대형 언어 모델의 상호 입출력 연동 절차 및 

전체적인 시스템의 구조를 정립, 구현하는 것을 목표로 합니다.

#### 2. 추천 시스템 및 대형 언어 모델에 대한 경량화 작업 수행
대형 언어 모델 선정과 추천 시스템 구축 과정에서 여러 가지 경량화 방식을 적용한 뒤,

성능과 자원 요구량 사이의 균형을 갖춘 시스템을 구축하는 것을 목표로 합니다.

#### 3. 최적의 추천 제공 서비스
사용자의 발화 내용에서 유용한 정보를 추출하고, 이를 기반으로 한 추천을 통하여 

각 사용자의 개인적 선호와 맥락에 일치하는 최적의 아이템(영화) 및 근거를 산출하는 서비스를 제공하는 것을 목표로 합니다.

### 프로젝트 주요 내용
#### 1. 데이터 전처리 및 추천 모듈 구현
* 추천 모듈에 활용될 수 있도록 영화와 평점 데이터들을 다중 레이블 특성 벡터화하였습니다.
* 이를 활용하여 사용자의 발화로부터 반영된 키워드와의 유사도를 계산하고, 별도의 신뢰도 점수를 연산한 뒤 이를 가중 결합하여 최종적으로 추천하는 아이템(영화)의 후보 목록을 산출하는 추천 모듈을 구현하였습니다.

#### 2. 대형 언어 모델의 적용
* EEVE-KR-Instruct 모델을 차용하였습니다,
* 차용된 대형 언어 모델은 사용자 발화 내용 분석에서부터 최종 추천 근거 생성에 이르기까지, 여러 요소에서 활용하였습니다.

#### 3. 데이터베이스-서버의 구현 및 서비스
* 사용자의 서비스 이용을 위한 서버를 구축하였습니다.
* 한 세션에서 그치는 것이 아닌, 지속적인 상호작용을 위하여 사용자의 주요 선호 정보를 저장하는 데이터베이스를 구축하였습니다.

---
# 2. 상세 설계

## 2.1. 시스템 구성도

![image](https://github.com/user-attachments/assets/3c96c77f-ceca-4972-a2ea-49bb9a1186e9)


## 2.2. 사용 기술
> ex) React.Js - React14, Node.js - v20.0.2
### Backend
* Flask
* MySQL
### Frontend
* React.Js
* CSS
### Server
* FastAPI
* LangChain

---
# 3. 설치 및 사용법

본 프로젝트는 Ubuntu 20.04 버전에서 개발되었으며 함께 포함된 다음의 스크립트를 수행하여 
관련 패키지들의 설치와 빌드를 수행할 수 있습니다.
```
$ ./install_and_build.sh
```

---
# 4. 소개 및 시연 영상
[![2024년 전기 졸업과제 26 LLecommend](http://img.youtube.com/vi/WqjpfN7P3K4/0.jpg)](https://www.youtube.com/watch?v=WqjpfN7P3K4&list=PLFUP9jG-TDp-CVdTbHvql-WoADl4gNkKj&index=26)

---
# 5. 팀 소개
### 박지환, mobush99@gmail.com
* 데이터 분석 및 전처리
* 추천 시스템 구축
* LLM 모델 선정 및 테스트
* 시스템 아키텍처 설계

### 장재혁, spiderman@marvel.com
* 백엔드 개발
* 결과 시각화
* API 설계 및 구현

### 하현진, 
* 프론트엔드 개발
* 웹 ui 구성
* 데이터 전처리
* 모델 서빙



## 2. 레파지토리 구성
- 레파지토리 내에 README.md 파일 생성하고 아래의 가이드라인과 작성팁을 참고하여 README.md 파일을 작성하세요. (이 레파지토리의 SAMPLE_README.md 참조)
- 레파지토리 내에 docs 디렉토리를 생성하고 docs 디렉토리 내에는 과제 수행 하면서 작성한 각종 보고서, 발표자료를 올려둡니다. (이 레파지토리의 docs 디렉토리 참조)
- 그 밖에 레파지토리의 폴더 구성은 과제 결과물에 따라 자유롭게 구성하되 가급적 코드의 목적이나 기능에 따라 디렉토리를 나누어 구성하세요.

---

## 3. 레파지토리 제출 

- **`[주의]` 레파지토리 제출**은 해당 레파지토리의 ownership을 **학과 계정**으로 넘기는 것이므로 되돌릴 수 없습니다.
- **레파지토리 제출** 전, 더 이상 수정 사항이 없는지 다시 한번 확인하세요.
- github 레파지토리에서 Settings > General > Danger zone > Transfer 클릭
  <img src="https://github.com/user-attachments/assets/cb2361d4-e07e-4b5d-9116-aa80dddd8a8b" alt="소유주 변경 경로" width="500" />
  
- [ Specify an organization or username ]에 'PNUCSE'를 입력하고 확인 메세지를 입력하세요.
  <img src="https://github.com/user-attachments/assets/7c63955d-dcfe-4ac3-bdb6-7d2620575f3a" alt="소유주 변경" width="400" />


## 5. README.md 작성팁 
* 마크다운 언어를 이용해 README.md 파일을 작성할 때 참고할 수 있는 마크다운 언어 문법을 공유합니다.  
* 다양한 예제와 보다 자세한 문법은 [이 문서](https://www.markdownguide.org/basic-syntax/)를 참고하세요.

### 5.1. 헤더 Header
```
# This is a Header 1
## This is a Header 2
### This is a Header 3
#### This is a Header 4
##### This is a Header 5
###### This is a Header 6
####### This is a Header 7 은 지원되지 않습니다.
```
<br />

### 5.2. 인용문 BlockQuote
```
> This is a first blockqute.
>	> This is a second blockqute.
>	>	> This is a third blockqute.
```
> This is a first blockqute.
>	> This is a second blockqute.
>	>	> This is a third blockqute.
<br />

### 5.3. 목록 List
* **Ordered List**
```
1. first
2. second
3. third  
```
1. first
2. second
3. third
<br />

* **Unordered List**
```
* 하나
  * 둘

+ 하나
  + 둘

- 하나
  - 둘
```
* 하나
  * 둘

+ 하나
  + 둘

- 하나
  - 둘
<br />

### 5.4. 코드 CodeBlock
* 코드 블럭 이용 '``'
```
여러줄 주석 "```" 이용
"```
#include <stdio.h>
int main(void){
  printf("Hello world!");
  return 0;
}
```"

단어 주석 "`" 이용
"`Hello world`"

* 큰 따움표(") 없이 사용하세요.
``` 
<br />

### 5.5. 링크 Link
```
[Title](link)
[부산대학교 정보컴퓨터공학부](https://cse.pusan.ac.kr/cse/index..do)

<link>
<https://cse.pusan.ac.kr/cse/index..do>
``` 
[부산대학교 정보컴퓨터공학부](https://cse.pusan.ac.kr/cse/index..do)

<https://cse.pusan.ac.kr/cse/index..do>
<br />

### 5.6. 강조 Highlighting
```
*single asterisks*
_single underscores_
**double asterisks**
__double underscores__
~~cancelline~~
```
*single asterisks* <br />
_single underscores_ <br />
**double asterisks** <br />
__double underscores__ <br />
~~cancelline~~  <br />
<br />

### 5.7. 이미지 Image
```
<img src="image URL" width="600px" title="Title" alt="Alt text"></img>
![Alt text](image URL "Optional title")
```
- 웹에서 작성한다면 README.md 내용 안으로 이미지를 드래그 앤 드롭하면 이미지가 생성됩니다.
- 웹이 아닌 로컬에서 작성한다면, github issue에 이미지를 드래그 앤 드롭하여 image url 을 얻을 수 있습니다. (URL만 복사하고 issue는 제출 안 함.)
  <img src="https://github.com/user-attachments/assets/0fe3bff1-7a2b-4df3-b230-cac4ef5f6d0b" alt="이슈에 image 올림" width="600" />
  <img src="https://github.com/user-attachments/assets/251c6d42-b36b-4ad4-9cfa-fa2cc67a9a50" alt="image url 복사" width="600" />


### 5.8. 유튜브 영상 추가
```markdown
[![영상 이름](유튜브 영상 썸네일 URL)](유튜브 영상 URL)
[![부산대학교 정보컴퓨터공학부 소개](http://img.youtube.com/vi/zh_gQ_lmLqE/0.jpg)](https://www.youtube.com/watch?v=zh_gQ_lmLqE)    
```
[![부산대학교 정보컴퓨터공학부 소개](http://img.youtube.com/vi/zh_gQ_lmLqE/0.jpg)](https://www.youtube.com/watch?v=zh_gQ_lmLqE)    

- 이때 유튜브 영상 썸네일 URL은 유투브 영상 URL로부터 다음과 같이 얻을 수 있습니다.

- `Youtube URL`: https://www.youtube.com/watch?v={동영상 ID}
- `Youtube Thumbnail URL`: http://img.youtube.com/vi/{동영상 ID}/0.jpg 
- 예를 들어, https://www.youtube.com/watch?v=zh_gQ_lmLqE 라고 하면 썸네일의 주소는 http://img.youtube.com/vi/zh_gQ_lmLqE/0.jpg 이다.

