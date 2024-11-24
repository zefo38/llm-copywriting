import pandas as pd
import re
from interest_calculator import filter_card_benefits_by_user_interest
# CSV 데이터 로드
def load_data():
    CategoryOfInterest = pd.read_csv('data/CategoryOfInterest.csv')
    log = pd.read_csv('data/Processed_Click_Log_Data.csv')
    CardCategory = pd.read_csv('data/CardCategory.csv')
    AnnualFee = pd.read_csv('data/카드실적.csv')
    MainCategory = pd.read_csv('data/대분류카테고리.csv')

    return CategoryOfInterest, log, CardCategory, AnnualFee, MainCategory
def load_recommendations():
    # 추천 데이터 파일 경로
    recommendations_path = "user_recommendations.csv"
    # CSV 파일 읽기
    return pd.read_csv(recommendations_path)

# 연회비 데이터에서 국내 연회비 추출
def extract_domestic_fee(fee_string):
    match = re.search(r'국내 (?:(\d+)만)?(\d*)천?원?', fee_string)
    if match:
        ten_thousand = int(match.group(1)) * 10000 if match.group(1) else 0
        thousand = int(match.group(2)) * 1000 if match.group(2) else 0
        return ten_thousand + thousand
    return 0

# 연회비 데이터 전처리
def preprocess_annual_fee(annual_fee_data):
    annual_fee_data['domestic_fee'] = annual_fee_data['annualfee'].apply(extract_domestic_fee)
    return annual_fee_data
# 카드와 대분류 데이터 병합 및 전처리
def preprocess_card_data(CardCategory, MainCategory):
    # 카드 데이터와 대분류 데이터 병합
    card = pd.merge(CardCategory, MainCategory, how='left', on='mainCtgId')

    # 카드별 mainCtgName과 mainCtgId 리스트 생성
    card_ctg_list = card.groupby('cardId').agg({
        'mainCtgId': list,
        'mainCtgName': list
    }).reset_index()
    # 리스트 데이터를 문자열로 변환
    card_ctg_list['mainCtgNameListStr'] = card_ctg_list['mainCtgName'].apply(lambda x: " ".join(x))
    
    return card_ctg_list

# 카드 혜택과 사용자 관심 병합
def get_filtered_card_data(user_id, combined_interest, card_ctg_list):
    filtered_cards = filter_card_benefits_by_user_interest(user_id, combined_interest, card_ctg_list)

    # 카드 ID, 이름, 혜택 필드만 유지
    filtered_cards = filtered_cards[['cardId', 'mainCtgNameListStr']]
    return filtered_cards
