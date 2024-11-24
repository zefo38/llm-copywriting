log = pd.read_csv('data/Processed_Click_Log_Data.csv')
CategoryOfInterest = pd.read_csv('data/CategoryOfInterest.csv')

# 사용자별 관심도점수 구하기

# 사용자의 관심 카테고리 개수 구하기 : 암묵적 관심도 점수 계산을 위해서
def calculate_user_interest_count(log):
    return log.groupby('userId')['mainCtgId'].count().reset_index()

# 사용자별 관심도 점수 모델링
def calculate_matching_scores(CategoryOfInterest, log_data, user_interest_count):
    matching_card = []
    log_data = log_data.sort_values('userId')
    for _, card_row in CategoryOfInterest.iterrows():
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