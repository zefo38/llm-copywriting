# LLM 기반 카드 추천 및 광고 생성 시스템
## 프로젝트 개요
이 프로젝트는 사용자 관심도와 카드 혜택 데이터를 기반으로 최적의 카드 추천과 창의적인 광고 문구 생성을 목표로 합니다. Python과 LLM(Large Language Model)을 활용하여 데이터를 분석하고 광고를 제작하며, 사용자 맞춤형 경험을 제공합니다.

## 주요 기능
**1. 카드 추천**
- 사용자 (클릭 로그 데이터 활용) 관심도를 기반으로 카드 점수 계산.
- 사용자의 명시적, 암묵적 관심도를 고려하여 맞춤형 카드 추천.

**2. 광고 문구 생성**

- 추천된 카드를 바탕으로 감성적이고 실용적인 광고 카피 생성.
- 카드의 주요 혜택을 강조하며, 이모티콘을 활용한 생동감 있는 문구 제공.

**3. 유사 카드 추천**

- 벡터화된 카드 데이터를 기반으로 코사인 유사도를 계산하여 가장 유사한 카드 추천.

**4. 데이터 전처리 및 관리**

- 연회비 데이터 전처리, 카드 혜택 데이터 병합.
- .gitignore를 활용하여 민감한 데이터를 보호.



```
project/
│
├── data/                         # 데이터 파일 (Git에서 무시)
│   ├── CategoryOfInterest.csv    # 사용자 관심도 데이터
│   ├── Processed_Click_Log_Data.csv  # 클릭 로그 데이터
│   ├── CardCategory.csv          # 카드 카테고리 데이터
│   ├── 카드정보.csv               # 카드 정보
│   └── 대분류카테고리.csv          # 대분류 카테고리 정보
├── ad_generator.py               # 광고 생성 로직
├── card_recommendation.py        # 카드 추천 알고리즘
├── contents.py                   # 카드 유사도 계산
├── data_handler.py               # 데이터 로드 및 전처리
├── interest_calculator.py        # 사용자 관심도 계산
├── main.py                       # 메인 실행 파일
└── requirements.txt              # 프로젝트 의존성
```


코드 설명
1. ad_generator.py
카드 이름과 혜택을 입력받아 LLM을 활용하여 광고 문구를 생성합니다​(ad_generator).
2. card_recommendation.py
사용자 관심도를 바탕으로 카드 점수를 계산하고, 가장 유사한 카드를 추천합니다​(card_recommendation).
3. contents.py
카드 데이터를 벡터화하고, 코사인 유사도를 계산하여 카드 간 유사성을 분석합니다​(contents).
4. data_handler.py
CSV 파일을 로드하고 데이터 전처리를 수행합니다. 연회비 데이터를 추출 및 변환합니다​(data_handler).
5. interest_calculator.py
사용자 관심도(명시적, 암묵적)를 계산하고, 이를 기반으로 카드를 필터링합니다​(interest_calculator).
6. main.py
전체 워크플로를 관리하며, 최종적으로 사용자에게 추천 카드 및 광고 문구를 출력합니다​(main).
