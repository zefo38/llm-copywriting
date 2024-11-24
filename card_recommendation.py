import pandas as pd
from ad_generator import generate_advertising_copy
from interest_calculator import filter_card_benefits_by_user_interest

# 카드별 점수 계산
def calculate_card_scores(card_category, combined_interest):
    card_category_grouped = card_category.groupby('cardId')['mainCtgId'].apply(list).reset_index()
    scores = []
    for _, card_row in card_category_grouped.iterrows():
        card_id = card_row['cardId']
        card_main_ctgs = card_row['mainCtgId']
        for _, user_row in combined_interest.iterrows():
            user_id = user_row['userId']
            user_main_ctg = user_row['mainCtgId']
            if user_main_ctg in card_main_ctgs:
                score = (
                    user_row['explicit_interest'] +
                    (user_row['implicit_interest'] / max(1, user_row['interest_count']))
                )
                scores.append({'cardId': card_id, 'userId': user_id, 'category_score': score})
    score_df = pd.DataFrame(scores)
    return score_df.groupby(['cardId', 'userId'])['category_score'].sum().reset_index()

# 사용자별 최고 점수 + 낮은 연회비 카드 선택
def select_top_card_with_low_fee(card_scores, annual_fee_data):
    card_scores = pd.merge(card_scores, annual_fee_data[['cardId', 'domestic_fee']], on='cardId', how='left')

    def select_best_card(group):
        max_score = group['category_score'].max()
        top_cards = group[group['category_score'] == max_score]
        if len(top_cards) > 1:
            return top_cards.loc[top_cards['domestic_fee'].idxmin()]
        return top_cards.iloc[0]

    top_cards = card_scores.groupby('userId').apply(select_best_card).reset_index(drop=True)
    return top_cards[['userId', 'cardId', 'category_score', 'domestic_fee']]


# 사용자별로 가장 유사한 카드 찾기
def get_most_similar_cards(top_cards, similarity_df, num_similar=3):
    recommendations = []

    for _, row in top_cards.iterrows():
        user_id = row['userId']
        card_id = row['cardId']

        # 유사도가 높은 카드를 찾고 정렬
        similar_cards = similarity_df.loc[card_id].sort_values(ascending=False)

        # 추천 카드 수 제한 (자기 자신 제외)
        similar_cards = similar_cards[similar_cards.index != card_id].head(num_similar)

        # 추천 결과 저장
        for similar_card_id, similarity in similar_cards.items():
            recommendations.append({
                "userId": user_id,
                "original_cardId": card_id,
                "recommended_cardId": similar_card_id,
                "similarity_score": similarity
            })

    # 추천 결과를 데이터프레임으로 반환
    return pd.DataFrame(recommendations)

# 추천된 카드에서 사용자 관심사 기반 혜택 필터링
def add_user_interest_to_recommendations(recommendations, combined_interest, card_ctg_list):
    filtered_recommendations = []

    for _, rec in recommendations.iterrows():
        user_id = rec['userId']
        recommended_card_id = rec['recommended_cardId']

        # 카드 데이터 필터링
        card_data = card_ctg_list[card_ctg_list['cardId'] == recommended_card_id]

        # 사용자 관심 카테고리에 해당하는 카드만 선택
        filtered_cards = filter_card_benefits_by_user_interest(user_id, combined_interest, card_data)
        
        if not filtered_cards.empty:
            filtered_recommendations.append({
                "userId": user_id,
                "recommended_cardId": recommended_card_id,
                "mainCtgNameListStr": filtered_cards.iloc[0]['mainCtgNameListStr']
            })

    return pd.DataFrame(filtered_recommendations)

def get_user_recommendations(user_id, recommendations, card_ctg_list):
    # 사용자 추천 카드 가져오기
    card_info = pd.read_csv("data/카드정보.csv")
    user_recommendations = recommendations[recommendations['userId'] == user_id]
    card_ctg_list = pd.merge(card_ctg_list, card_info[['cardId', 'cardName']], on='cardId', how='left')
    # 카드 이름과 혜택 매핑
    ad_results = []
    for _, rec in user_recommendations.iterrows():
        card_id = rec['recommended_cardId']
        card_data = card_ctg_list[card_ctg_list['cardId'] == card_id]

        if not card_data.empty:
            card_name = card_data.iloc[0]['cardName']  # 카드 이름 또는 ID
            benefits = card_data.iloc[0]['mainCtgNameListStr']  # 혜택 문자열

            # 광고 문구 생성
            ad_copy = generate_advertising_copy(card_name, benefits)
            ad_results.append({
                "cardId": card_id,
                "cardName": card_name,
                "benefits": benefits,
                "adCopy": ad_copy
            })
    return pd.DataFrame(ad_results)