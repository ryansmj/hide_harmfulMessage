import time
import os
import cv2
from capture_window import capture_specific_window
from text_to_png import text_to_image, check_words

def main():
    window_title = input("감시할 창의 제목을 입력하세요: ")
    # 감시할 단어 입력
    target_words = input("감시할 단어를 쉼표로 구분하여 입력하세요: ").split(',')
    
    # 공백 제거
    target_words = [word.strip() for word in target_words]

    # 각 단어에 대해 이미지 생성
    output_folder = 'images'  # 이미지 저장 폴더
    image_paths = []  # 생성된 이미지 경로 저장할 리스트
    for word in target_words:
        image_path = text_to_image(text=word, output_folder=output_folder)  # 각 단어로 이미지 생성
        image_paths.append(image_path)  # 이미지 경로 추가

    while True:
            # 스크린샷 캡처
            screenshot_path = capture_specific_window(window_title)
            if screenshot_path:
                print(f'Screenshot saved at: {screenshot_path}')
                # 각 이미지와 스크린샷 비교
                for image_path in image_paths:
                    if check_words(image_path, screenshot_path):
                        print("타겟 단어가 감지되었습니다!")
                        return  # 감지된 경우 루프 종료

            time.sleep(1)  # 1초 간격으로 캡처

if __name__ == '__main__':
    main()
