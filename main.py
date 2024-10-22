from capture_window import capture_specific_window
from checkWord import check_for_words
import time

def main():
    window_title = input("감시할 창의 제목을 입력하세요: ")
    
    while True:
        # 스크린샷 캡처
        screenshot_path = capture_specific_window(window_title)
        if screenshot_path:
            print(f'Screenshot saved at: {screenshot_path}')
            # 단어 체크 함수 호출 
            if check_for_words(screenshot_path):  # 단어 리스트 제거
                print("목표 단어가 감지되었습니다.")
                break  # 감지된 경우 루프 종료

        time.sleep(1)  # 1초 간격으로 캡처

if __name__ == '__main__':
    main()
