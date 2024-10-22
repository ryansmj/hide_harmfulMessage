import pyautogui
import time

def right_click_at_coordinates(x, y):
    """
    주어진 좌표에서 마우스 우클릭을 수행합니다.

    :param coordinates: (x, y) 좌표 튜플
    """
    pyautogui.moveTo(x, y)  # 마우스를 해당 좌표로 이동
    time.sleep(0.5)  # 약간의 지연 후
    pyautogui.rightClick()  # 우클릭
    # 스크롤 100만큼 내리기
    pyautogui.move(20, 215)
    time.sleep(0.5)
    pyautogui.move(100, 0)
    pyautogui.leftClick()
    time.sleep(0.5)
    pyautogui.moveTo(320, 360)
    pyautogui.leftClick()


def scrolldown():
    pyautogui.moveTo(380, 200)
    pyautogui.leftClick()
    pyautogui.scroll(-250)  # 음수 값을 사용하여 스크롤을 아래로 내림


