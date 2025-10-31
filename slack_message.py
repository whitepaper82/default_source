# 위에서 만든 slack_sender.py 파일에서 함수를 가져옵니다.
from slack_sender import send_slack_message

# 1. .env 파일에 설정된 기본 채널로 메시지 보내기
print("기본 채널로 알림 전송 시도...")
user_name = "jslee82"
success = send_slack_message("자동화 작업이 완료되었습니다.","jslee82")

if success:
    print("알림 전송 성공!")
else:
    print("알림 전송 실패!")