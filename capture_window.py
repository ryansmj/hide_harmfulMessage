import time
import cv2
import numpy as np
import pyautogui
from pywinauto import Application
import win32gui
import os
import pytesseract  # Tesseract OCR 모듈

def restore_and_focus_window(window_title):
    try:
        app = Application().connect(title=window_title)
        window = app[window_title]
        
        # 최소화된 창을 복원합니다.
        if not window.is_visible():
            window.restore()

        # 창을 포그라운드로 가져옵니다. 
        window.set_focus()
        time.sleep(1)  # 포커싱 후 잠시 대기

        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
        else:
            print("해당 제목의 창을 찾을 수 없습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

def capture_specific_window(window_title, save_folder='screenshots'):
    restore_and_focus_window(window_title)

    # 창의 위치와 크기를 가져옵니다.
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print("해당 제목의 창을 찾을 수 없습니다.")
        return None

    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    width = rect[2] - rect[0]  # 오른쪽 - 왼쪽
    height = rect[3] - rect[1]  # 아래쪽 - 위쪽

    # 스크린샷을 캡처합니다.
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot_np = np.array(screenshot)
    screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    # 저장할 폴더가 존재하는지 확인하고, 없으면 생성합니다.
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 이미지 파일로 저장
    screenshot_path = os.path.join(save_folder, f'screenshot_{int(time.time())}.png')  # 파일 경로 지정
    cv2.imwrite(screenshot_path, screenshot_rgb)

    return screenshot_path  # 이미지 경로 반환

