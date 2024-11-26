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
def get_most_similar_cards(top_cards, similarity_df, num_similar=2):
    recommendations = []

    for _, row in top_cards.iterrows():
        user_id = row['userId']
        card_id = row['cardId']

        # 유사도가 높은 카드를 찾고 정렬 (자기 자신 포함)
        similar_cards = similarity_df.loc[card_id].sort_values(ascending=False)

        # 자기 자신 카드를 포함하고 num_similar개의 카드만 선택
        top_similar_cards = similar_cards.head(num_similar)

        # 추천 결과 저장
        for similar_card_id, similarity in top_similar_cards.items():
            recommendations.append({
                "userId": user_id,
                "original_cardId": card_id,
                "recommended_cardId": similar_card_id,
                "similarity_score": similarity
            })

    # 추천 결과를 데이터프레임으로 반환
    return pd.DataFrame(recommendations)

# 추천된 카드에서 사용자 관심사 기반 혜택 필터링
def add_user_interest_to_recommendations(recommendations, combined_interest, card_ctg_list,main_category):
    filtered_recommendations = []

    for _, rec in recommendations.iterrows():
        user_id = rec['userId']
        recommended_card_id = rec['recommended_cardId']
        
        # 카드 데이터 필터링
        card_data = card_ctg_list[card_ctg_list['cardId'] == recommended_card_id]

        # 사용자 관심 카테고리에 해당하는 카드만 선택
        filtered_cards = filter_card_benefits_by_user_interest(user_id, combined_interest, card_data)
        filtered_cards["intersectionMapped"] = filtered_cards["intersection"].apply(
    lambda ids: [main_category.loc[main_category["mainCtgId"] == int(id), "mainCtgName"].values[0] for id in ids]
)
        if not filtered_cards.empty:
            filtered_recommendations.append({
                "userId": user_id,
                "recommended_cardId": recommended_card_id,
                "mainCtgNameListStr": filtered_cards.iloc[0]['intersectionMapped']
            })
        print(f"해당하는 DF 확인 : {filtered_cards}")
    return pd.DataFrame(filtered_recommendations)

