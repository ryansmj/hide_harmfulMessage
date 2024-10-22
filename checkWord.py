import pytesseract
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def check_for_words(screenshot_path, target_words):
    """
    스크린샷에서 지정된 단어를 감지하여 출력하고, 감지된 단어를 강조하여 저장합니다.

    :param screenshot_path: 스크린샷의 경로
    :param target_words: 감시할 단어 목록
    """
    # 스크린샷 이미지 로드
    screenshot = cv2.imread(screenshot_path)

    # 이미지 전처리
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # OCR 수행 (한글 및 영어 언어 설정)
    custom_config = r'--oem 3 --psm 6 -l kor+eng'
    text = pytesseract.image_to_string(binary_img, config=custom_config)
    print("읽은 텍스트:", text)

    # 강조된 이미지를 저장할 폴더 생성
    checked_folder = 'screenshots_Checked'
    if not os.path.exists(checked_folder):
        os.makedirs(checked_folder)

    # Matplotlib을 사용하여 강조 표시
    fig, ax = plt.subplots()
    ax.imshow(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))

    # 입력된 단어 목록을 반복하여 텍스트에서 검색
    for word in target_words:
        if word in text:
            print(f'경고! "{word}" 단어가 감지되었습니다.')
            data = pytesseract.image_to_data(binary_img, config=custom_config, output_type=pytesseract.Output.DICT)

            # 모든 인식된 단어와 좌표 출력 및 강조 표시
            for i, detected_word in enumerate(data['text']):
                if detected_word.strip() == word:  # 정확히 일치하는 경우
                    (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                    print(f'인식된 단어: "{detected_word}", 좌표: (x: {x}, y: {y}, w: {w}, h: {h})')

                    # 사각형 추가
                    rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='green', facecolor='none')
                    ax.add_patch(rect)

            # 강조된 이미지 저장
            highlighted_path = os.path.join(checked_folder, os.path.basename(screenshot_path).replace('.png', '_highlighted.png'))
            plt.axis('off')
            plt.savefig(highlighted_path, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            print(f'강조된 이미지 저장: {highlighted_path}')
            return True

    # 감지된 단어가 없으면 False 반환
    return False
