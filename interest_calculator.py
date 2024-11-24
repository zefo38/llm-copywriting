import pandas as pd

# 명시적 관심도 계산
def calculate_explicit_interest(category_of_interest):
    return category_of_interest.groupby(['userId', 'mainCtgId']).size().reset_index(name='explicit_interest')

# 암묵적 관심도 계산
def calculate_implicit_interest(log):
    return log.groupby(['userId', 'mainCtgId']).size().reset_index(name='implicit_interest')

# 사용자별 관심 카테고리 수 계산
def calculate_user_interest_count(combined_interest):
    return combined_interest.groupby('userId')['mainCtgId'].count().reset_index(name='interest_count')

# 명시적/암묵적 관심도 병합
def merge_interests(explicit_interest, implicit_interest):
    combined = pd.merge(explicit_interest, implicit_interest, on=['userId', 'mainCtgId'], how='outer').fillna(0)
    combined['explicit_interest'] = combined['explicit_interest'].astype(int)
    combined['implicit_interest'] = combined['implicit_interest'].astype(int)
    return combined


# 사용자 관심사로 카드 데이터 필터링
def filter_card_benefits_by_user_interest(user_id, combined_interest, card_ctg_list):
    # 특정 사용자 관심 카테고리 추출
    user_interest_categories = combined_interest[combined_interest['userId'] == user_id]['mainCtgId'].unique()

    # 카드별 혜택에서 사용자 관심 카테고리만 필터링
    filtered_cards = card_ctg_list[card_ctg_list['mainCtgId'].apply(
        lambda categories: any(ctg_id in user_interest_categories for ctg_id in categories)
    )]
    
    return filtered_cards

