import pandas as pd

log = pd.read_csv('data/Processed_Click_Log_Data.csv')
customer = pd.read_csv('data/user_category_mapping.csv')
card = pd.read_csv('data/카드실적.csv')


def calculate_interest(log: pd.DataFrame, customer: pd.DataFrame) -> pd.DataFrame:

    # 고객 데이터를 기준으로 명시적 관심도 데이터프레임 생성
    interest_data = customer.copy()
    interest_data['명시적관심도'] = 1
    interest_data['암묵적관심도'] = 0

    # 로그 데이터에서 암묵적 관심도 계산
    implicit_interest = (
        log.groupby(['user_id', 'mainCtgId'])['event_type']
        .count()
        .reset_index(name='암묵적관심도')
    )
    implicit_interest['명시적관심도'] = 0

    # 관심 데이터를 암묵적 관심 데이터와 병합
    result = pd.concat([implicit_interest, interest_data], ignore_index=True)

    # 동일 user_id, mainCtgName에 대해 암묵적 관심도와 명시적 관심도를 통합
    result = (
        result.groupby(['user_id', 'mainCtgId'], as_index=False)
        .agg({'암묵적관심도': 'max', '명시적관심도': 'max'})
    )

    # 정렬
    result = result.sort_values(['user_id', 'mainCtgId']).reset_index(drop=True)

    return result

# user 별 관심도 데이터
interests = calculate_interest(log, customer)


def extract_domestic_fee(fee_string):
  import re
  # 국내 금액만 추출
  match = re.search(r'국내 (?:(\d+)만)?(\d*)천?원?', fee_string)
  if match:
    # '만'과 '천'단위 합산해서 숫자로 변환
    ten_thousand = int(match.group(1)) * 10000 if match.group(1) else 0
    thousand = int(match.group(2)) * 1000 if match.group(2) else 0
    return ten_thousand + thousand
  return 0 # 국내 금액이 없으면 0 반환

# 카드 연회비 데이터
card['Domestic_Fee'] = card['annualfee'].apply(extract_domestic_fee)
# # ----------------------------------------------------------------------
CardCategory = pd.read_csv("data/CardCategory.csv")


# merge_outer = pd.merge(CardCategory,MainCategory, how='left',on='mainCtgId')
matching_card= []
count = interests.groupby('user_id')['mainCtgId'].count().reset_index()
for i, card_row in CardCategory.iterrows():
  total_score = 0
  for idx, user_row in interests.iterrows():
    score = 0
    # 카드의 혜택 카테고리와 사용자의 관심 카테고리 비교
    if user_row['mainCtgId'] == card_row['mainCtgId']:

      # 암묵적 관심도 점수
      if user_row['암묵적관심도'] >= 1:
        user_count = count[count['user_id'] == user_row['user_id']]['mainCtgId'].values[0]
        score += user_row['암묵적관심도'] / user_count
      if user_row['명시적관심도'] == 1:
        score += user_row['명시적관심도']

        # 매칭 데이터 기록
    matching_card.append({
            'userId': user_row['user_id'],
            'mainCtgId': card_row['mainCtgId'],
            'cardId': card_row['cardId'],
            'matching_score': score
        })

matching_card_df = pd.DataFrame(matching_card)

# 카드별 총 점수 계산
final_scores = matching_card_df.groupby(['userId','cardId']).agg({
    'matching_score': 'sum'
}).reset_index()

print(final_scores)


final =pd.merge(final_scores, card, how='left',on='cardId')
print(final)
sorted_data = final.groupby(['userId','cardId'])[['matching_score','Domestic_Fee']].sum().sort_values(by=['userId','matching_score','Domestic_Fee'],ascending=[True,False,False])
card_selected = sorted_data.reset_index().sort_values(['userId','matching_score','Domestic_Fee'],ascending=[True, False, True]).groupby('userId').head(
  1
)
print(card_selected)