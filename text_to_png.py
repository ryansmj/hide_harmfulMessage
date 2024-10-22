from PIL import Image, ImageDraw, ImageFont
import os
import re
import cv2
import pytesseract

# 16진수 색상을 RGB로 변환하는 함수
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_next_image_index(output_folder):
    # 폴더 내 파일 목록 가져오기
    existing_files = os.listdir(output_folder)
    # 'check_png'로 시작하는 파일명에서 숫자 추출
    indices = [
        int(re.search(r'check_png(\d+)', f).group(1)) 
        for f in existing_files 
        if re.search(r'check_png(\d+)', f)
    ]
    # 가장 큰 숫자에 1을 더한 값을 반환, 없으면 1 반환
    return max(indices, default=0) + 1

def text_to_image(text, font_path='C:/Windows/Fonts/malgun.ttf', font_size=50, bg_color='#ffffff', text_color='#191919', output_folder='images'):
    # 배경색과 글자색을 16진수에서 RGB로 변환
    bg_color_rgb = hex_to_rgb(bg_color)
    text_color_rgb = hex_to_rgb(text_color)

    # 폰트 설정
    font = ImageFont.truetype(font_path, font_size)

    # 텍스트 크기 계산
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # 여백을 추가한 이미지 생성
    padding = 30  # 여유 공간
    image = Image.new('RGB', (text_width + padding * 2, text_height + padding * 2), color=bg_color_rgb)

    # 텍스트 그리기
    draw = ImageDraw.Draw(image)
    draw.text((padding, padding), text, font=font, fill=text_color_rgb)

    # 저장할 폴더가 존재하는지 확인하고, 없으면 생성합니다.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 다음 이미지 인덱스 찾기
    next_index = get_next_image_index(output_folder)

    # 이미지 저장
    output_image_path = os.path.join(output_folder, f'check_png{next_index}.png')
    image.save(output_image_path)
    print(f"이미지가 '{output_image_path}'로 저장되었습니다.")
    return output_image_path

def preprocess_image(image_path):
    # 이미 전처리된 파일이면 처리하지 않음
    if '_preprocessed' in image_path:
        return image_path  # 이미 전처리된 파일이므로 경로를 그대로 반환

    # 이미지를 OpenCV로 읽기
    screenshot = cv2.imread(image_path)
    
    # 이미지 전처리
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 처리된 이미지 저장 경로 설정
    preprocessed_image_path = image_path.replace('.png', '_preprocessed.png')
    
    # 처리된 이미지 저장
    cv2.imwrite(preprocessed_image_path, binary_img)
    
    return preprocessed_image_path  # 전처리된 이미지 경로 반환


def ocr_from_images_in_folder(folder_path):
    custom_config = r'--oem 3 --psm 6 -l kor+eng'
    all_text = ""
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".png"):  # .png 파일만 처리
            image_path = os.path.join(folder_path, file_name)
            processed_image_path = preprocess_image(image_path)  # 이미지 전처리
            text = pytesseract.image_to_string(processed_image_path, config=custom_config).strip()  # OCR 수행 및 공백 제거
            all_text += text + " "  # 추출된 텍스트를 결합
    return all_text.strip()  # 마지막 공백 제거 후 반환

def check_words(image_path_2, images_folder='images'):
    # text1에는 images 폴더 안에 있는 모든 이미지에서 추출한 텍스트를 담습니다.
    text1 = ocr_from_images_in_folder(images_folder)
    
    # 이미지 전처리 및 text2 추출
    image_path_2_processed = preprocess_image(image_path_2)
    custom_config = r'--oem 3 --psm 6 -l kor+eng'
    text2 = pytesseract.image_to_string(image_path_2_processed, config=custom_config).strip()
    
    print("첫 번째 이미지 텍스트:", text1)

    words_from_text2 = set(text2.split())  # 두 번째 이미지의 단어 목록 생성

    for word in text1.split():
        print("카톡 : " , words_from_text2, " 끝 카톡")
        print("어디야: ", word, " :끝")
        if word in words_from_text2:
            print(f"'{word}' found in the second image.")
            return True

    print("No words from the first image found in the second image.")
    return False
