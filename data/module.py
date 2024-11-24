import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 데이터 로드 함수
def load_data():
    log = pd.read_csv('data/Processed_Click_Log_Data.csv')
    customer = pd.read_csv('data/CategoryOfInterest.csv')
    card = pd.read_csv('data/카드실적.csv')
    card_category = pd.read_csv('data/CardCategory.csv')
    small_category = pd.read_csv('data/소분류.csv')
    large_category = pd.read_csv('data/대분류카테고리.csv')
    return log, customer, card, card_category, small_category, large_category

# 사용자 관심도별 카운트 계산
def calculate_user_interest_count(log):
    return log.groupby('userId')['mainCtgId'].count().reset_index()

# # 카드 정보와 사용자 관심 혜택 카테고리 
# def merge_user_card_data(card, customer):
#     return pd.merge(card, customer, on='userId', how='inner')

# 매칭 점수 계산
def calculate_matching_scores(card_data, log_data, user_interest_count):
    matching_card = []
    for _, card_row in card_data.iterrows():
        for _, log_row in log_data.iterrows():
            score = 0
            if log_row['mainCtgId'] == card_row['mainCtgId']:
                if log_row['암묵적관심도'] >= 1:
                    user_count = user_interest_count[user_interest_count['userId'] == log_row['userId']]['mainCtgId'].values[0]
                    score += log_row['암묵적관심도'] / user_count
                if log_row['명시적관심도'] == 1:
                    score += log_row['명시적관심도']
                matching_card.append({
                    'userId': log_row['userId'],
                    'mainCtgId': card_row['mainCtgId'],
                    'cardId': card_row['cardId'],
                    'matching_score': score
                })
    return pd.DataFrame(matching_card)

# 카드별 총 점수 계산
def calculate_final_scores(matching_card_df):
    return matching_card_df.groupby(['userId', 'cardId']).agg({'matching_score': 'sum'}).reset_index()

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

# 카드 정보 변환 (LLM 입력용)
def prepare_card_info_for_llm(top_card, card_category):
    card_info = pd.merge(top_card, card_category, on='cardId', how='left')
    card_info['llm_input'] = card_info.apply(
        lambda x: f"- 카드 이름: {x['cardName']}\n- 혜택: {x['mainCtgName']}",
        axis=1
    )
    return "\n\n".join(card_info['llm_input'])
