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
    padding = 20  # 여유 공간
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
    # 이미지를 OpenCV로 읽기
    screenshot = cv2.imread(image_path)
    
    # 이미지 전처리
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 처리된 이미지 저장 (디버깅용)
    preprocessed_image_path = image_path.replace('.png', '_preprocessed.png')
    cv2.imwrite(preprocessed_image_path, binary_img)
    
    return preprocessed_image_path

def check_words(image_path_1, image_path_2):
    # 이미지 전처리
    image_path_1_processed = preprocess_image(image_path_1)
    image_path_2_processed = preprocess_image(image_path_2)

    # 전처리한 이미지 보기
    img1 = cv2.imread(image_path_1_processed)
    img2 = cv2.imread(image_path_2_processed)

    cv2.imshow('Processed Image 1', img1)
    cv2.imshow('Processed Image 2', img2)
    
    # 키 입력 대기 (창을 닫기 위해)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # OCR 수행 (한글 및 영어 언어 설정)
    custom_config = r'--oem 3 --psm 6 -l kor+eng'

    # 첫 번째 이미지에서 텍스트 추출
    text1 = pytesseract.image_to_string(image_path_1_processed, config=custom_config).strip()  # 공백 제거
    # 두 번째 이미지에서 텍스트 추출
    text2 = pytesseract.image_to_string(image_path_2_processed, config=custom_config).strip()  # 공백 제거

    print("첫 번째 이미지 텍스트:", text1)


    words_from_text2 = set(text2.split())  # 두 번째 이미지의 단어 목록 생성

    for word in text1.split():
        print("카톡 : " , words_from_text2, " 끝 카톡")
        print("어디야: ", word, " :끝")
        if word in words_from_text2:  # 두 번째 이미지의 단어 목록과 비교
            
            print(f"'{word}' found in the second image.")
            return True  # 단어가 발견되면 True 반환

    print("No words from the first image found in the second image.")
    return False  # 단어가 발견되지 않으면 False 반환
