import tkinter as tk
import time
from threading import Thread
from capture_window import capture_specific_window
from check_word import check_words, add_check_word, load_check_words

class WordMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("단어 감시 프로그램")

        # 창 크기 설정 (너비 400, 높이 300)
        master.geometry("400x300")  # 너비 x 높이
        master.resizable(True, True)  # 크기 조정 가능

        self.window_title_label = tk.Label(master, text="감시할 창의 제목:")
        self.window_title_label.pack(pady=(10, 0))  # 상단 여백 추가

        self.window_title_entry = tk.Entry(master)
        self.window_title_entry.pack(pady=5)

        self.word_label = tk.Label(master, text="감시할 단어 추가:")
        self.word_label.pack(pady=(10, 0))

        self.word_entry = tk.Entry(master)
        self.word_entry.pack(pady=5)

        self.add_word_button = tk.Button(master, text="단어 추가", command=self.add_word)
        self.add_word_button.pack(pady=(5, 10))

        self.screenshot_label = tk.Label(master, text="스크린샷 경로:")
        self.screenshot_label.pack(pady=(10, 0))

        self.screenshot_display = tk.Label(master, text="")
        self.screenshot_display.pack(pady=5)

        self.start_monitoring_button = tk.Button(master, text="감시 시작", command=self.start_monitoring)
        self.start_monitoring_button.pack(pady=(5, 10))

        self.pause_button = tk.Button(master, text="일시정지", command=self.toggle_pause)
        self.pause_button.pack(pady=(5, 10))

        self.exit_button = tk.Button(master, text="종료", command=self.exit_program)
        self.exit_button.pack(pady=(5, 10))

        # 체크 단어 파일 경로
        self.check_word_file = 'checkword.txt'
        self.existing_words = load_check_words(self.check_word_file)

        self.is_paused = False  # 일시정지 상태 변수
        self.monitoring_thread = None  # 모니터링 스레드 변수

    def add_word(self):
        target_word = self.word_entry.get()
        if target_word:
            if target_word in self.existing_words:
                print(f"'{target_word}'은(는) 이미 등록된 단어입니다.")
            else:
                add_check_word(self.check_word_file, target_word)
                self.existing_words.append(target_word)
                print(f"'{target_word}'이(가) 체크 단어 목록에 추가되었습니다.")
                self.word_entry.delete(0, tk.END)  # 입력창 비우기

    def start_monitoring(self):
        window_title = self.window_title_entry.get()
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
            self.monitoring_thread = Thread(target=self.monitor_words, args=(window_title,))
            self.monitoring_thread.start()

    def toggle_pause(self):
        """일시정지/재개 기능을 토글하는 함수"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="재개")  # 버튼 텍스트 변경
            print("감시가 일시정지되었습니다.")
        else:
            self.pause_button.config(text="일시정지")  # 버튼 텍스트 변경
            print("감시가 재개되었습니다.")

    def monitor_words(self, window_title):
        try:
            while True:
                if self.is_paused:
                    time.sleep(1)  # 일시정지 상태일 때 1초 대기
                    continue

                # 스크린샷 캡처
                screenshot_path = capture_specific_window(window_title)
                if screenshot_path:
                    self.screenshot_display.config(text=screenshot_path)  # 경로 표시
                    if check_words(screenshot_path, self.check_word_file):
                        print("단어가 감지되었습니다!")
                else:
                    print(f"창 '{window_title}'을 찾을 수 없습니다. 다시 시도 중...")
                
                time.sleep(1)  # 1초 간격으로 캡처 및 감시 진행
        except KeyboardInterrupt:
            print("\n프로그램이 종료되었습니다.")

    def exit_program(self):
        self.master.quit()  # 프로그램 종료


if __name__ == '__main__':
    root = tk.Tk()
    app = WordMonitorApp(root)
    root.mainloop()
