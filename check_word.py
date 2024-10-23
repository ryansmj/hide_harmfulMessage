import os
import cv2
import pytesseract
import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from hide_message import right_click_at_coordinates, scrolldown

# 로그 설정
logging.basicConfig(filename='check_word.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_image(image_path):
    if '_preprocessed' in image_path:
        return image_path  # 이미 전처리된 파일이면 경로 반환

    # 이미지를 OpenCV로 읽기
    screenshot = cv2.imread(image_path)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 전처리된 이미지 저장
    preprocessed_image_path = image_path.replace('.png', '_preprocessed.png')
    cv2.imwrite(preprocessed_image_path, binary_img)
    
    return preprocessed_image_path

def ocr_from_image(image_path):
    custom_config = r'--oem 3 --psm 6 -l kor+eng'
    processed_image_path = preprocess_image(image_path)

    if processed_image_path is None:
        return "", []  # 전처리 실패 시 빈 문자열과 빈 리스트 반환

    try:
        # 이미지에서 텍스트와 위치 정보를 추출
        data = pytesseract.image_to_data(processed_image_path, config=custom_config, output_type=pytesseract.Output.DICT)
    except Exception as e:
        logging.error(f"OCR 처리 중 오류 발생: {e}")
        print(f"OCR 처리 중 오류 발생: {e}")
        return "", []

    text = ""
    boxes = []
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 0:  # 신뢰도(confidence)가 0보다 큰 경우에만
            text += data['text'][i] + " "
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            boxes.append((x, y, w, h))  # 사각형의 좌표 저장

    return text.strip(), boxes  # 텍스트와 사각형 좌표 반환

def load_check_words(file_path):
    if not os.path.exists(file_path):
        open(file_path, 'w').close()  # 파일이 존재하지 않으면 생성
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().rstrip(',') for line in f.read().split(',') if line.strip()]

def add_check_word(file_path, new_word):
    existing_words = load_check_words(file_path)
    if new_word in existing_words:
        print(f"'{new_word}'은(는) 이미 등록된 단어입니다.")
        return  # 중복이면 종료
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"{new_word}, ")  # 단어 추가

def check_words(image_path, check_word_file='checkword.txt'):
    check_words = load_check_words(check_word_file)
    
    text_from_image, boxes = ocr_from_image(image_path)

    # 텍스트가 비어 있는지 확인
    if not text_from_image.strip():
        print("이미지에서 텍스트가 감지되지 않았습니다.")
        return False  # 텍스트가 없으면 False 반환

    # Matplotlib로 이미지 표시 및 사각형 그리기
    fig, ax = plt.subplots(1)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Matplotlib에서 RGB 형식 사용
    ax.imshow(image)

    # split 결과 저장
    words_in_image = text_from_image.split()
    boxes_length = len(boxes)  # boxes의 길이 확인

    for word in check_words:
        print(f"비교 중: '{word}'")
        # 부분 문자열 비교로 수정
        if word in text_from_image:  # 이제 부분 문자열이 있을 경우에도 감지
            print(f"'{word}'이(가) 이미지에서 감지되었습니다.")
            # 감지된 단어에 해당하는 사각형만 그리기
            for i in range(len(words_in_image)):
                # 감지된 단어가 words_in_image[i]의 부분 문자열인지 확인
                if word in words_in_image[i] and i < boxes_length:  
                    (x, y, w, h) = boxes[i]  # 해당 단어의 박스 가져오기
                    rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='red', facecolor='none')  # 빨간색 사각형
                    ax.add_patch(rect)  # Matplotlib에 사각형 추가

                    # x, y가 정의되었을 때만 클릭 시도
                    right_click_at_coordinates(x, y)

            # 변경된 이미지를 저장
            output_image_path = image_path.replace('.png', '_marked.png')
            plt.axis('off')  # 축 숨기기
            plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)  # 이미지 저장
            plt.close(fig)  # 그래프 닫기
            return True  # 타겟 단어 감지 시 True 반환

    print("이미지에서 감지된 단어가 없습니다.")
    scrolldown()
    return False

def remove_check_word(file_path, word):
    """파일에서 체크 단어를 삭제하는 함수."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # 삭제할 단어가 포함된 줄을 제외한 리스트 생성
        updated_lines = [line for line in lines if line.strip() != word]

        # 파일에 업데이트된 내용 저장
        with open(file_path, 'w') as file:
            file.writelines(updated_lines)

    except Exception as e:
        print(f"단어 삭제 중 오류 발생: {e}")
