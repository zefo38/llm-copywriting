import pandas as pd

# 데이터 로드 함수
def load_data(card_data_path, user_interest_data_path):
    card_data = pd.read_csv(card_data_path)
    user_interest_data = pd.read_csv(user_interest_data_path)
    return card_data, user_interest_data

# 사용자 관심도별 카운트 계산
def calculate_user_interest_count(user_interest_data):
    return user_interest_data.groupby('user_id')['mainCtgId'].count().reset_index()

# 매칭 점수 계산
def calculate_matching_scores(card_data, user_interest_data, user_interest_count):
    matching_card = []

    for _, card_row in card_data.iterrows():
        for _, user_row in user_interest_data.iterrows():
            score = 0
            # 카드와 사용자의 mainCtgId 비교
            if user_row['mainCtgId'] == card_row['mainCtgId']:
                # 암묵적 관심도 점수
                if user_row['암묵적관심도'] >= 1:
                    user_count = user_interest_count[user_interest_count['user_id'] == user_row['user_id']]['mainCtgId'].values[0]
                    score += user_row['암묵적관심도'] / user_count
                # 명시적 관심도 점수
                if user_row['명시적관심도'] == 1:
                    score += user_row['명시적관심도']
                # 매칭 데이터 기록
                matching_card.append({
                    'userId': user_row['user_id'],
                    'mainCtgId': card_row['mainCtgId'],
                    'cardId': card_row['cardId'],
                    'matching_score': score
                })

    return pd.DataFrame(matching_card)

# 카드별 총 점수 계산
def calculate_final_scores(matching_card_df):
    return matching_card_df.groupby(['userId', 'cardId']).agg({
        'matching_score': 'sum'
    }).reset_index()

# 카드 점수와 세부 정보 병합 및 정렬
def merge_and_sort_scores(final_scores, card_data):
    final = pd.merge(final_scores, card_data, how='left', on='cardId')
    sorted_data = final.groupby(['userId', 'cardId'])[['matching_score', 'Domestic_Fee']].sum().sort_values(
        by=['userId', 'matching_score', 'Domestic_Fee'], ascending=[True, False, False]
    )
    return sorted_data.reset_index()

# 최적 카드 선택
def select_top_card(sorted_data):
    return sorted_data.sort_values(['userId', 'matching_score', 'Domestic_Fee'], ascending=[True, False, True]).groupby('userId').head(1)

# 메인 실행 함수
def main(card_data_path, user_interest_data_path):
    # 데이터 로드
    card_data, user_interest_data = load_data(card_data_path, user_interest_data_path)
    
    # 사용자 관심 카테고리 개수 계산
    user_interest_count = calculate_user_interest_count(user_interest_data)
    
    # 매칭 점수 계산
    matching_card_df = calculate_matching_scores(card_data, user_interest_data, user_interest_count)
    
    # 카드별 점수 집계
    final_scores = calculate_final_scores(matching_card_df)
    
    # 카드 데이터 병합 및 정렬
    sorted_data = merge_and_sort_scores(final_scores, card_data)
    
    # 사용자별 최적 카드 선택
    top_card = select_top_card(sorted_data)
    
    return top_card
