from card_matching import main

# 파일 경로 설정
card_data_path = "path/to/card_data.csv"  # 카드 데이터 경로
user_interest_data_path = "path/to/user_interest_data.csv"  # 사용자 관심 데이터 경로

# 실행
top_card_df = main(card_data_path, user_interest_data_path)

# 결과 출력
print(top_card_df)

# 결과 저장
output_path = "Selected_Top_Card.csv"
top_card_df.to_csv(output_path, index=False)
print(f"Top card data saved to {output_path}")
