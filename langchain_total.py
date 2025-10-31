from dotenv import load_dotenv
import os

# LangChain core
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# LLMs
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

# Slack sender (사용자 모듈)
from slack_sender import send_slack_message

# ------------------------------------------------------------------
# 0) 환경 변수 로드
#    - OPENAI_API_KEY, (필요 시) 프록시/추가 설정 등
#    - OLLAMA는 로컬 base_url 사용
# ------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------
# 1) LLM 초기화
# ------------------------------------------------------------------
llm_ollama = ChatOllama(
    base_url="http://localhost:11434",  # 필요 시 'http://192.168.1.10:12345' 등으로 변경
    model="gemma3:1b"
)

llm_openai = ChatOpenAI(model="gpt-4o-mini")  # OPENAI_API_KEY 필요

# ------------------------------------------------------------------
# 2) 1단계 프롬프트 (사용자 입력 → Ollama)
# ------------------------------------------------------------------
user_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# Ollama 체인: 문자열로 바로 파싱
ollama_chain = user_prompt | llm_ollama | StrOutputParser()

# ------------------------------------------------------------------
# 3) 2단계 프롬프트 (Ollama 응답 → Slack용 요약/메시지화)
# ------------------------------------------------------------------
slack_prompt = ChatPromptTemplate.from_template(
    "아래 결과는 ollama의 응답 결과입니다. "
    "이 내용을 분석하여 슬랙으로 보낼 한국어 메시지로 간결하게 만들어주세요.\n\n"
    "### 요청 추론 응답:\n{ollama_answer}\n\n"
    "출력 형식: 한두 문장, 핵심만."
)

slack_chain = slack_prompt | llm_openai | StrOutputParser()

# ------------------------------------------------------------------
# 4) 전체 파이프라인 (LCEL로 연결)
#     입력: {input}
#     출력: slack_message (문자열)
# ------------------------------------------------------------------
full_chain = (
    {"ollama_answer": ollama_chain}  # 먼저 Ollama 결과 생성
    | slack_chain                    # 그 결과를 Slack 메시지로 변환
)

# ------------------------------------------------------------------
# 5) 실행 및 Slack 전송
# ------------------------------------------------------------------
if __name__ == "__main__":
    # 예시 입력
    query = "대한민국의 수도는 어디인가요?"

    # 전체 체인 실행 (Ollama → OpenAI 요약)
    slack_message = full_chain.invoke({"input": query})

    # 콘솔 확인
    print("\n[Slack Message Preview]\n", slack_message)

    # Slack 전송 (채널/사용자 지정)
    target = "jslee82"  # 채널/사용자 식별자에 맞게 사용하세요
    print("\n기본 채널로 알림 전송 시도...")
    success = send_slack_message(slack_message, target)

    if success:
        print("알림 전송 성공!")
    else:
        print("알림 전송 실패!")
