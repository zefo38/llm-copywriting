import pandas as pd
def calculate_card_scores(CategoryOfInterest, Log, card_data):
    # 사용자 관심 카테고리와 로그에서 categoryId 추출
    user_categories = pd.concat([
        CategoryOfInterest['categoryId'],
        Log['categoryId']
    ]).unique()

    # 카드별 점수 계산
    scores = []
    for _, card in card_data.iterrows():
        card_id = card['cardId']
        benefits = card['benefits']  # 카드의 혜택 리스트

        # 카드의 혜택 카테고리와 사용자 카테고리 간 교집합 크기 계산
        matching_categories = [b for b in benefits if b['categoryId'] in user_categories]
        score = len(matching_categories)

        scores.append({
            "cardId": card_id,
            "score": score
        })

    return pd.DataFrame(scores)
