import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# 카드 혜택 데이터를 벡터화
def vectorize_card_data(card_ctg_list):
    vectorizer = CountVectorizer()
    ctg_matrix = vectorizer.fit_transform(card_ctg_list['mainCtgNameListStr'])
    return ctg_matrix, vectorizer.get_feature_names_out()
    
# 코사인 유사도 계산
def calculate_card_similarity(ctg_matrix, card_ctg_list):
    cate_sim = cosine_similarity(ctg_matrix, ctg_matrix)
    similarity_df = pd.DataFrame(cate_sim, index=card_ctg_list['cardId'], columns=card_ctg_list['cardId'])
    return similarity_df
