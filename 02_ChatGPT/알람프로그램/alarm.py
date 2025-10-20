import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import mysql.connector
import pygame
import threading
import datetime
import time
import os
from win10toast import ToastNotifier

# MySQL 연결 설정
conn = mysql.connector.connect(
    host="localhost",
    user="aloha",
    password="123456",
    database="aloha"
)
cursor = conn.cursor()

# alarm 테이블 생성
cursor.execute('''CREATE TABLE IF NOT EXISTS alarm (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    datetime DATETIME,
                    sound VARCHAR(255)
                )''')
conn.commit()

# pygame 초기화
pygame.mixer.init()

# 알림 함수 (별도 스레드로 실행)
def show_notification(title, msg):
    def _toast():
        n = ToastNotifier()
        n.show_toast(title, msg, duration=5, threaded=False)
    threading.Thread(target=_toast, daemon=True).start()

# 알람 클래스
class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("알람 관리 프로그램")
        self.root.geometry("600x500")

        self.alarm_frame = ttk.Frame(root)
        self.alarm_frame.pack(fill="both", expand=True)

        ttk.Label(self.alarm_frame, text="🔔 알람 관리 대시보드", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self.alarm_frame, columns=("name", "datetime", "sound"), show='headings')
        self.tree.heading("name", text="알람 이름")
        self.tree.heading("datetime", text="알람 시간")
        self.tree.heading("sound", text="소리 파일")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.edit_alarm)

        btn_frame = ttk.Frame(self.alarm_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="➕ 알람 추가", command=self.add_alarm_window).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="🗑️ 삭제", command=self.delete_alarm).grid(row=0, column=1, padx=5)

        self.load_alarms()
        self.start_alarm_checker()

        # 알람 상태 관리
        self.is_alarm_playing = False
        self.alarm_popup = None

    def load_alarms(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cursor.execute("SELECT * FROM alarm")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row[1:])

    def add_alarm_window(self):
        win = tk.Toplevel(self.root)
        win.title("알람 추가")
        win.geometry("400x300")

        ttk.Label(win, text="알람 이름").pack(pady=5)
        name_entry = ttk.Entry(win)
        name_entry.pack(pady=5)

        ttk.Label(win, text="날짜 선택").pack(pady=5)
        date_entry = DateEntry(win, date_pattern='yyyy-mm-dd')
        date_entry.pack(pady=5)

        ttk.Label(win, text="시간 선택 (HH:MM)").pack(pady=5)
        time_entry = ttk.Entry(win)
        time_entry.pack(pady=5)

        ttk.Label(win, text="소리 파일 선택").pack(pady=5)
        sounds = [f for f in os.listdir('C:/alarm') if f.endswith('.mp3')]
        sound_var = tk.StringVar(value="기본.mp3")
        sound_combo = ttk.Combobox(win, textvariable=sound_var, values=sounds, state="readonly")
        sound_combo.pack(pady=5)

        def save_alarm():
            name = name_entry.get()
            date = date_entry.get()
            time_str = time_entry.get()
            sound = os.path.join('C:/alarm', sound_var.get())
            alarm_time = f"{date} {time_str}:00"
            cursor.execute("INSERT INTO alarm (name, datetime, sound) VALUES (%s, %s, %s)", (name, alarm_time, sound))
            conn.commit()
            win.destroy()
            self.load_alarms()

        ttk.Button(win, text="저장", command=save_alarm).pack(pady=10)

    def delete_alarm(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("선택 없음", "삭제할 알람을 선택하세요.")
            return
        name = self.tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM alarm WHERE name=%s", (name,))
        conn.commit()
        self.load_alarms()

    def edit_alarm(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected)['values']
        if not values:
            return

        win = tk.Toplevel(self.root)
        win.title("알람 수정")
        win.geometry("400x300")

        ttk.Label(win, text="알람 이름").pack(pady=5)
        name_entry = ttk.Entry(win)
        name_entry.insert(0, values[0])
        name_entry.pack(pady=5)

        ttk.Label(win, text="날짜 선택").pack(pady=5)
        date_entry = DateEntry(win, date_pattern='yyyy-mm-dd')
        date_entry.set_date(values[1].split(' ')[0])
        date_entry.pack(pady=5)

        ttk.Label(win, text="시간 선택 (HH:MM)").pack(pady=5)
        time_entry = ttk.Entry(win)
        time_entry.insert(0, values[1].split(' ')[1][:5])
        time_entry.pack(pady=5)

        ttk.Label(win, text="소리 파일 선택").pack(pady=5)
        sounds = [f for f in os.listdir('C:/alarm') if f.endswith('.mp3')]
        sound_var = tk.StringVar(value=os.path.basename(values[2]))
        sound_combo = ttk.Combobox(win, textvariable=sound_var, values=sounds, state="readonly")
        sound_combo.pack(pady=5)

        def update_alarm():
            name = name_entry.get()
            date = date_entry.get()
            time_str = time_entry.get()
            sound = os.path.join('C:/alarm', sound_var.get())
            alarm_time = f"{date} {time_str}:00"
            cursor.execute("UPDATE alarm SET datetime=%s, sound=%s WHERE name=%s", (alarm_time, sound, values[0]))
            conn.commit()
            win.destroy()
            self.load_alarms()

        ttk.Button(win, text="수정 저장", command=update_alarm).pack(pady=10)

    def start_alarm_checker(self):
        def check():
            while True:
                cursor.execute("SELECT name, datetime, sound FROM alarm")
                for (name, alarm_time, sound) in cursor.fetchall():
                    now = datetime.datetime.now().replace(second=0, microsecond=0)
                    if now == alarm_time:
                        show_notification("알람", f"{name} - {alarm_time}")
                        self.show_alarm_popup(name, sound)
                time.sleep(30)
        threading.Thread(target=check, daemon=True).start()

    def show_alarm_popup(self, name, sound_path):
        if self.alarm_popup and self.alarm_popup.winfo_exists():
            return  # 이미 팝업이 열려있으면 무시

        self.alarm_popup = tk.Toplevel(self.root)
        self.alarm_popup.title("⏰ 알림")
        self.alarm_popup.geometry("300x150")
        self.alarm_popup.attributes("-topmost", True)

        tk.Label(
            self.alarm_popup,
            text=f"{name} 알람이 울립니다!",
            font=("맑은 고딕", 14, "bold")
        ).pack(pady=20)

        tk.Button(
            self.alarm_popup,
            text="알람 종료",
            font=("맑은 고딕", 12),
            bg="#ff5555",
            fg="white",
            relief="flat",
            command=self.stop_alarm_sound
        ).pack(pady=10)

        threading.Thread(target=self.play_alarm_sound, args=(sound_path,), daemon=True).start()

    def play_alarm_sound(self, sound_path):
        self.is_alarm_playing = True
        play_count = 0
        pygame.mixer.init()
        while self.is_alarm_playing and play_count < 5:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and self.is_alarm_playing:
                time.sleep(0.1)
            play_count += 1
        pygame.mixer.quit()
        self.is_alarm_playing = False

    def stop_alarm_sound(self):
        self.is_alarm_playing = False
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        if self.alarm_popup and self.alarm_popup.winfo_exists():
            self.alarm_popup.destroy()

# 메인 실행
if __name__ == '__main__':
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()