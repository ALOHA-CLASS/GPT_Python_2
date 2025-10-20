import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
from datetime import datetime

# 음성 변환 엔진 초기화
engine = pyttsx3.init()

# GUI 구성
root = tk.Tk()
root.title("텍스트 음성 변환기")
root.geometry("400x300")

# 텍스트 입력
text_label = tk.Label(root, text="텍스트 입력:")
text_label.pack(pady=10)

text_entry = tk.Text(root, height=5, width=40)
text_entry.pack(pady=5)

# 음성 변환 함수
def convert_to_speech():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("경고", "텍스트를 입력해주세요.")
        return

    # 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    short_text = text[:10].replace(' ', '')  # 처음 10글자
    filename = f"{timestamp}_{short_text}.mp3"

    # 파일 저장 경로 선택
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", initialfile=filename,
                                             filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        engine.save_to_file(text, file_path)
        engine.runAndWait()
        messagebox.showinfo("완료", f"음성 파일이 저장되었습니다:\n{file_path}")
    else:
        messagebox.showinfo("취소", "파일 저장이 취소되었습니다.")

# 변환 버튼
convert_button = tk.Button(root, text="음성 변환", command=convert_to_speech)
convert_button.pack(pady=20)

root.mainloop()
