import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CardCategory = pd.read_csv('data/CardCategory.csv')
MainCategory = pd.read_csv('data/대분류카테고리.csv')

card = pd.merge(CardCategory, MainCategory, how='left', on='mainCtgId')
card_df = card.groupby('cardId')['mainCtgName'].apply(list).reset_index()
card_df.rename(columns={'mainCtgName': 'categoryList'}, inplace=True)

card_df['categoryList'] = card_df['categoryList'].apply(lambda x: " ".join(x))

# CountVectorizer 설정
vectorizer = CountVectorizer()

# 문자열 데이터를 벡터화
X = vectorizer.fit_transform(card_df['categoryList'])

count_vect = CountVectorizer(ngram_range=(1,2))
category_matrix = count_vect.fit_transform(card_df['categoryList'])
category_matrix

category_matrix.toarray()


cate_sim = cosine_similarity(category_matrix, category_matrix)
cate_sim.shape

cate_sim[0, :20]

card_sim_sorted_index = cate_sim.argsort()[:, ::-1]

def find_sim_card(df, sorted_index, cardId, top_n = 2):

  # 2. 찾고자 하는 카드의 인덱스 찾기
  
  similar_indexes = sorted_index[cardId, :top_n]

  similar_indexes = similar_indexes.reshape(-1) # 1차원 배열로 만들어 주기

  return df.iloc[similar_indexes]

similar_card_df = find_sim_card(card_df, card_sim_sorted_index,1)

print(similar_card_df)

