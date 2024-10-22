import time
import os
from capture_window import capture_specific_window
from check_word import check_words, add_check_word, load_check_words
import warnings

def main():
    warnings.filterwarnings("ignore", category=UserWarning)
    
    window_title = input("감시할 창의 제목을 입력하세요: ")
    
    # 체크 단어 파일 경로
    check_word_file = 'checkword.txt'
    
    # 이미 등록된 단어 로드
    existing_words = load_check_words(check_word_file)

    while True:
        # 감시할 단어 입력
        target_word = input("감시할 단어를 입력하세요 (종료하려면 'exit' 입력): ")
        if target_word.lower() == 'exit':
            break
        
        # 중복 체크
        if target_word in existing_words:
            print(f"'{target_word}'은(는) 이미 등록된 단어입니다.")
        else:
            # 단어를 파일에 추가
            add_check_word(check_word_file, target_word)
            existing_words.append(target_word)  # 기존 단어 목록에 추가
            print(f"'{target_word}'이(가) 체크 단어 목록에 추가되었습니다.")

    try:
        word_detected = False  # 단어 감지 여부를 저장할 변수
        while True:
            # 스크린샷 캡처
            screenshot_path = capture_specific_window(window_title)
            if screenshot_path:
                # 이미지에서 단어 감지
                if check_words(screenshot_path, check_word_file):
                    word_detected = True  # 단어가 감지되면 True로 설정
            else:
                print(f"창 '{window_title}'을 찾을 수 없습니다. 다시 시도 중...")

            time.sleep(1)  # 1초 간격으로 캡처 및 감시 진행
            
    except KeyboardInterrupt:
        print("\n프로그램이 종료되었습니다.")        

if __name__ == '__main__':
    main()
