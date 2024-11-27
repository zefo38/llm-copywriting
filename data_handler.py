import requests
import pandas as pd

BASE_URL = "http://example.com/api"  # 실제 API URL로 변경

def load_user_interest_data():
    try:
        # 사용자 관심 데이터 가져오기
        category_response = requests.post(f"{BASE_URL}/category-of-interest")
        category_data = category_response.json()
        CategoryOfInterest = pd.DataFrame(category_data)

        # 사용자 행동 로그 가져오기
        log_response = requests.post(f"{BASE_URL}/logs")
        log_data = log_response.json()
        Log = pd.DataFrame(log_data)

        return CategoryOfInterest, Log
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch user interest data: {str(e)}")


def load_card_data():
    try:
        # 전체 카드 데이터 가져오기
        response = requests.post(f"{BASE_URL}/cards-with-benefits", json={})
        card_data = response.json()
        return pd.DataFrame(card_data)
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch card data: {str(e)}")
