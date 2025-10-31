from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
import langchain
from langchain_openai import ChatOpenAI

# 슬랙 메시지 전송
from slack_sender import send_slack_message
#from slack_sender import send_slack_message
load_dotenv()


# 2. Ollama 채팅 모델 초기화
llm_ollama = ChatOllama(
    base_url="http://localhost:11434",
    model="gemma3:1b"
)

# 3. 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# 4. LangChain Expression Language (LCEL)을 사용해 체인 구성
chain = prompt | llm_ollama

# 5. 체인 실행
response = chain.invoke({"input": "대한민국의 수도는 어디인가요?"})

# content 속성으로 결과 확인
print(response)

##### OpenAI

prompt = f"아래 결과는 ollama의 응답 결과에 대한 내용 입니다. \
이 내용을 분석하여 슬랙으로 보낼 메시지로 만들어주세요. \
    ### 요청 추론 응답 : {response}" 

llm_openai = ChatOpenAI(model="gpt-4o")
response = llm_openai.invoke(prompt)



##### 슬랙 메시지 보내기기
print("기본 채널로 알림 전송 시도...")
user_name = "jslee82"
success = send_slack_message(response.content,"jslee82")

if success:
    print("알림 전송 성공!")
else:
    print("알림 전송 실패!")