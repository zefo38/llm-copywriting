from data_handler import load_user_interest_data, load_card_data
from interest_calculator import calculate_card_scores
from flask import Flask, jsonify
from ad_generator import generate_ads_for_user

app = Flask(__name__)

@app.route("/recommend", methods=["GET"])
def recommend_cards():
    try:
        # 사용자 관심 데이터와 행동 로그 가져오기
        CategoryOfInterest, Log = load_user_interest_data()

        # 전체 카드 데이터 가져오기
        card_data = load_card_data()

        # 카드 점수 계산
        card_scores = calculate_card_scores(CategoryOfInterest, Log, card_data)

        # 상위 5개 카드 추천
        top_cards = card_scores.sort_values(by='score', ascending=False).head(5)

        # 추천 카드 정보 가져오기
        recommendations = card_data[card_data['cardId'].isin(top_cards['cardId'])]

        # 광고 생성
        ads = generate_ads_for_user(recommendations)

        # 결과 반환
        return jsonify(ads.to_dict(orient="records"))
    except Exception as e:
        app.logger.error(f"Error recommending cards: {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
