import pyautogui
import datetime
import os
import time

def capture_left_half_screenshot(save_path='screenshots'):
    """
    현재 화면의 좌측 절반을 캡처하여 지정된 경로에 저장합니다.

    :param save_path: 스크린샷을 저장할 디렉토리
    :return: 저장된 스크린샷의 파일 경로
    """
    # 디렉토리가 없으면 생성 
    if not os.path.exists(save_path):
        os.makedirs(save_path)


    # 현재 화면의 크기 가져오기
    screen_width, screen_height = pyautogui.size()

    time.sleep(2)

    # 좌측 절반 영역 계산
    left_half = (0, 0, screen_width // 2, screen_height)

    # 현재 시간으로 파일 이름 생성
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_filename = os.path.join(save_path, f'screenshot_{timestamp}.png')

    # 좌측 절반 스크린샷 캡처 및 저장
    screenshot = pyautogui.screenshot(region=left_half)
    screenshot.save(screenshot_filename)

    return screenshot_filename

if __name__ == '__main__':
    # 테스트: 스크린샷 캡처 및 경로 출력
    screenshot_path = capture_left_half_screenshot()
    print(f'Screenshot saved at: {screenshot_path}')
