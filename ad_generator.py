import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# 사용자별 필터링된 카드 데이터로 광고 문구 생성
def generate_ads_for_user(recommendations):
    ads = []
    for _, card in recommendations.iterrows():
        # 카드 이름과 첫 번째 혜택의 카테고리 이름을 광고 문구로 사용
        ad_copy = f"{card['cardName']}로 {card['benefits'][0]['categoryName']} 혜택을 누리세요!"
        ads.append({
            "cardId": card['cardId'],  # 카드 ID 추가 (필요하면)
            "adCopy": ad_copy
        })
    return pd.DataFrame(ads)





# 광고 문구 생성 함수
def generate_advertising_copy(card_name, benefits):
    print(card_name, benefits)
    # LLM 모델 설정
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7,
        streaming=True  # 스트리밍 출력
    )

    # 프롬프트 템플릿
    prompt_template = """
    당신은 뛰어난 광고 카피라이터입니다. 주어진 카드 정보와 혜택을 바탕으로 창의적이고 감동적인 카피라이팅 문구를 제작하는 것이 역할입니다.
    - 당신의 문구는 사용자에게 카드의 가치를 한눈에 전달할 수 있어야 하며, 읽는 사람이 혜택을 즉각적으로 이해하고 매력을 느끼게 해야 합니다.
    - 당신의 문구는 단순한 정보 전달이 아니라, 감정적인 연결을 만들어내야 합니다.
    - 사용자가 이 카드를 소유했을 때 느낄 수 있는 만족감을 생생하게 그려주세요.
    - 구체적인 혜택을 중심으로 재미있고 톡톡 튀는 문구를 작성해주세요.
    - 이모티콘을 더해서 산뜻하고 생동감 있는 문구를 만들어주세요.

    작성 시 참고할 핵심 요소 :
    1. 카드의 혜택과 특징을 한 문장으로 임팩트 있게 전달합니다.
    2. 사용자에게 긍정적이고 매력적인 이미지를 상상하게 합니다.
    3. 상황에 따라 "감성적인 접근" 또는 "실용적인 접근"으로 나뉘어 작성할 수 있습니다.

    요청사항:
    입력된 카드 정보 각각에 대해 1개의 톡톡 튀는 광고 문구를 작성해주세요.
    각 문구는 다음을 포함해야 합니다:
    - 카드의 주요 혜택 여러개 강조
    - 감성적 또는 실용적 요소
    - 이모티콘으로 생동감 추가
    - 40대 남성이 친근감을 느낄만한 문구로 제작

    카드 정보:
    - 카드 이름: {card_name}
    - 혜택: {benefits}

    작성할 문구:
    """

    # 프롬프트 템플릿 생성
    prompt = PromptTemplate(template=prompt_template)

    # RunnableMap 생성
    llm_chain = prompt | llm

    # LLM 실행
    formatted_input = {"card_name": card_name, "benefits": benefits}
    response = llm_chain.invoke(formatted_input)

    return str(response)