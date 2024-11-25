from data_handler import load_data, preprocess_annual_fee,preprocess_card_data,load_recommendations
from interest_calculator import (
    calculate_explicit_interest,
    calculate_implicit_interest,
    calculate_user_interest_count,
    merge_interests,
)
from contents import vectorize_card_data, calculate_card_similarity
from card_recommendation import (calculate_card_scores, 
                                 select_top_card_with_low_fee,
                                 get_most_similar_cards,
                                 add_user_interest_to_recommendations)
import pandas as pd
from ad_generator import generate_ads_for_user


def main():
    # 카드 정보 데이터 로드
    card_info = pd.read_csv("data/카드정보.csv")
    # 데이터 로드
    CategoryOfInterest, log, CardCategory, AnnualFee,MainCategory = load_data()

    # 연회비 데이터 전처리
    AnnualFee = preprocess_annual_fee(AnnualFee)

    # 관심도 계산
    explicit_interest = calculate_explicit_interest(CategoryOfInterest)
    implicit_interest = calculate_implicit_interest(log)
    combined_interest = merge_interests(explicit_interest, implicit_interest)

    # 사용자별 관심 카테고리 수 추가
    user_interest_count = calculate_user_interest_count(combined_interest)
    combined_interest = pd.merge(combined_interest, user_interest_count, on='userId', how='left')
    # 카드별 점수 계산
    card_scores = calculate_card_scores(CardCategory, combined_interest)

    # 사용자별 최적 카드 추천
    top_cards = select_top_card_with_low_fee(card_scores, AnnualFee)


       # 데이터 전처리
    card_ctg_list = preprocess_card_data(CardCategory, MainCategory)
#     # 카드 혜택 벡터화
    ctg_matrix, feature_names = vectorize_card_data(card_ctg_list)

#     # 카드 간 유사도 계산
    similarity_df = calculate_card_similarity(ctg_matrix, card_ctg_list)

#     # 사용자별로 유사 카드 추천
    recommendations = get_most_similar_cards(top_cards, similarity_df, num_similar=3)

    # 추천 카드에서 사용자 관심 혜택 필터링
    filtered_recommendations = add_user_interest_to_recommendations(recommendations, combined_interest, card_ctg_list,MainCategory)

        # 사용자 입력 받기
    user_id = int(input("Enter the user ID: ").strip())

    # 사용자 ID로 광고 생성
    ad_results = generate_ads_for_user(user_id, filtered_recommendations, card_info)
    pd.set_option('display.max_colwidth', None)
    # 결과 출력
    print(ad_results[["userId", "adCopy"]])
if __name__ == "__main__":
    main()
