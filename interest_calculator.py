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


def filter_card_benefits_by_user_interest(user_id, combined_interest, card_ctg_list):
    # 특정 사용자 관심 카테고리 추출
    user_interest_categories = combined_interest[combined_interest['userId'] == user_id]['mainCtgId'].unique()

    # 카드별 혜택에서 사용자 관심 카테고리와의 교집합 계산
    card_ctg_list['intersection'] = card_ctg_list['mainCtgId'].apply(
        lambda categories: list(set(categories) & set(user_interest_categories))
    )

    # 교집합이 비어있지 않은 카드만 필터링
    filtered_cards = card_ctg_list[card_ctg_list['intersection'].apply(len) > 0]

    # 사용자별 결과 추가
    filtered_cards['userId'] = user_id

    # 결과 반환
    return filtered_cards


def filter_all_users(combined_interest, card_ctg_list):
    # 사용자별 결과를 누적할 리스트
    all_filtered_cards = []

    # 사용자 ID 리스트 추출
    user_ids = combined_interest['userId'].unique()

    # 각 사용자별 필터링 수행
    for user_id in user_ids:
        filtered_cards = filter_card_benefits_by_user_interest(user_id, combined_interest, card_ctg_list)
        all_filtered_cards.append(filtered_cards)

    # 결과를 하나의 DataFrame으로 병합
    return pd.concat(all_filtered_cards, ignore_index=True)


