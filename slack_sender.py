# install 
# pip install slack_sdk
# pip install python-dotenv

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# --- 설정 (스크립트 로드 시 1회 실행) ---

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# .env 환경 변수에서 토큰과 기본 채널을 불러옵니다.
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
DEFAULT_CHANNEL = os.getenv("SLACK_CHANNEL")

# WebClient 인스턴스 생성
if not SLACK_BOT_TOKEN:
    print("오류: .env 파일에 SLACK_BOT_TOKEN이 설정되지 않았습니다.")
    # 토큰이 없으면 client를 None으로 설정
    slack_client = None
else:
    slack_client = WebClient(token=SLACK_BOT_TOKEN)

# --- 함수 정의 ---

def send_slack_message(message_text,user_name='',channel=None):
    """
    Slack 채널에 메시지를 전송하는 함수입니다.

    Args:
        message_text (str): 전송할 메시지 내용.
        channel (str, optional): 메시지를 보낼 채널 ID 또는 채널 이름. 
                                 None이면 .env의 SLACK_CHANNEL 값을 사용합니다.

    Returns:
        bool: 메시지 전송 성공 시 True, 실패 시 False.
    """
    
    # 1. Slack 클라이언트가 제대로 초기화되었는지 확인
    if slack_client is None:
        print("오류: Slack 클라이언트가 초기화되지 않았습니다. SLACK_BOT_TOKEN을 확인하세요.")
        return False

    # 2. 전송할 채널 결정
    target_channel = channel if channel else DEFAULT_CHANNEL
    
    if not target_channel:
        print("오류: 메시지를 보낼 채널이 지정되지 않았습니다.")
        print(".env에 SLACK_CHANNEL을 설정하거나, 함수 호출 시 channel 매개변수를 제공하세요.")
        return False

    # 3. 메시지 전송 시도
    try:
        # chat_postMessage API 호출
        response = slack_client.chat_postMessage(
            channel=target_channel,
            text=message_text + ' ' + user_name
        )
        print(f"메시지가 채널 '{target_channel}'에 성공적으로 전송되었습니다.")
        return True
    except SlackApiError as e:
        # API 호출 실패 시 에러 출력
        print(f"메시지 전송에 실패했습니다: {e.response['error']}")
        return False

# --- 함수 사용 예시 ---
if __name__ == "__main__":
    # 이 파일(slack_sender.py)을 직접 실행할 때만 아래 코드가 동작합니다.
    
    print("--- 1. 기본 채널(.env)로 테스트 메시지 전송 ---")
    test_message_1 = "안녕하세요! 함수를 통해 보내는 테스트 메시지입니다." + " [by jslee82]"
    send_slack_message(test_message_1)

    print("\n--- 2. 특정 채널(예: '#random')을 지정하여 테스트 메시지 전송 ---")
    test_message_2 = "이 메시지는 '#random' 채널로 갑니다."
    # send_slack_message(test_message_2, channel="#random") # 테스트 시 주석 해제