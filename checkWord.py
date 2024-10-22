import cv2
import numpy as np
import os 

def check_for_words(screenshot_path):
    """
    스크린샷에서 지정된 단어의 이미지와 비교하여 감지된 단어를 출력합니다.

    :param screenshot_path: 스크린샷의 경로
    """
    # 스크린샷 이미지 로드
    screenshot = cv2.imread(screenshot_path)

    # 감지할 단어 이미지 파일 경로 목록
    target_words_images = [f for f in os.listdir('images') if f.endswith('.png')]

    # 각 이미지에 대해 비교
    for word_image_name in target_words_images:
        word_image_path = os.path.join('images', word_image_name)
        word_image = cv2.imread(word_image_path)

        if word_image is None:
            print(f'경고! "{word_image_name}" 단어에 대한 이미지 파일을 찾을 수 없습니다.')
            continue

        # 이미지 비교를 위한 템플릿 매칭
        result = cv2.matchTemplate(screenshot, word_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # 유사도 임계값
        loc = np.where(result >= threshold)

        # 감지된 위치가 있는지 확인
        if loc[0].size > 0:
            print(f'경고! "{word_image_name}" 단어가 감지되었습니다. 프로그램을 종료합니다.')
            return True  # 감지된 경우 True 반환

    return False  # 감지되지 않은 경우 False 반환
