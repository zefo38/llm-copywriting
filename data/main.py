from module import (
    load_data,
    calculate_user_interest_count,
    merge_user_card_data,
    calculate_matching_scores,
    calculate_final_scores,
    merge_and_sort_scores,
    select_top_card,
    prepare_card_info_for_llm
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def main():
    # 데이터 로드
    log, customer, card, card_category, small_category, large_category = load_data()

    # 사용자 관심도 계산
    user_interest_count = calculate_user_interest_count(log)

    # 카드-사용자 데이터 병합
    card_data = merge_user_card_data(card, customer)

    # 매칭 점수 계산
    matching_card_df = calculate_matching_scores(card_data, log, user_interest_count)

    # 최종 점수 집계
    final_scores = calculate_final_scores(matching_card_df)

    # 점수 병합 및 정렬
    sorted_data = merge_and_sort_scores(final_scores, card)

    # 사용자별 최적 카드 선택
    top_card = select_top_card(sorted_data)

    print(top_card)
    # LLM에서 user_id를 입력받아 매칭된 카드 가져오기
    # user_id = 1
    # user_filtered_card = top_card[top_card['userId'] == int(user_id)]

    # if user_filtered_card.empty:
    #     print(f"해당 user_id({user_id})와 매칭된 카드가 없습니다.")
    #     return

    # # LLM 입력 데이터 준비
    # llm_input = prepare_card_info_for_llm(user_filtered_card, card_category)

    # LLM 입력 데이터 준비
    llm_input = prepare_card_info_for_llm(top_card, card_category)

    # LLM 모델 설정
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7,
        streaming=True
    )

    # 프롬프트 템플릿
    prompt_template = """
    당신은 뛰어난 광고 카피라이터입니다. 주어진 카드 정보와 혜택을 바탕으로 창의적이고 감동적인 카피라이팅 문구를 제작하는 것이 역할입니다.
    {llm_input}
    작성할 문구:
    """
    prompt = PromptTemplate(input_variables=["llm_input"], template=prompt_template)

    # LLM Chain 생성
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # LLM 실행
    response = llm_chain.run({"llm_input": llm_input})
    print("생성된 광고 문구:\n", response)

if __name__ == "__main__":
    main()
