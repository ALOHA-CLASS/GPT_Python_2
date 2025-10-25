import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Entry, Text, Button, END
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import time

# DB 설정
DB_CONFIG = {
    'host': 'localhost',
    'user': 'python',
    'password': '123456',
    'database': 'python'
}

# email 테이블 생성 함수
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email (
            id INT AUTO_INCREMENT PRIMARY KEY,
            recipient VARCHAR(255),
            subject VARCHAR(255),
            content TEXT,
            status VARCHAR(50) DEFAULT '전송전'
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# 이메일 등록 함수
def add_email(recipient, subject, content):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO email (recipient, subject, content) VALUES (%s, %s, %s)", (recipient, subject, content))
    conn.commit()
    cursor.close()
    conn.close()

# 이메일 수정 함수
def update_email(email_id, recipient, subject, content):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE email SET recipient=%s, subject=%s, content=%s WHERE id=%s
    """, (recipient, subject, content, email_id))
    conn.commit()
    cursor.close()
    conn.close()

# 이메일 삭제 함수
def delete_email(email_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM email WHERE id=%s", (email_id,))
    conn.commit()
    cursor.close()
    conn.close()

# 이메일 리스트 가져오기 (전송전 상태만)
def get_pending_emails():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM email WHERE status='전송전'")
    emails = cursor.fetchall()
    cursor.close()
    conn.close()
    return emails

# 상태 업데이트 함수
def mark_email_as_sent(email_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("UPDATE email SET status='완료' WHERE id=%s", (email_id,))
    conn.commit()
    cursor.close()
    conn.close()

# 이메일 전송 함수
def send_emails(driver):
    emails = get_pending_emails()
    for email in emails:
        driver.get("https://mail.naver.com/v2/new")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "recipient_input_element"))).send_keys(email['recipient'])
        driver.find_element(By.ID, "subject_title").send_keys(email['subject'])
        
        driver.find_element(By.CLASS_NAME, "button_write_task").click()

        WebDriverWait(driver, 10).until(EC.url_contains("/v2/new/done"))

        mark_email_as_sent(email['id'])
        # 대기시간 : 10초
        time.sleep(10)

    messagebox.showinfo("완료", "모든 이메일 전송을 완료했습니다.")

# 로그인 함수
def login_to_naver(driver, user_id, user_pw):
    driver.get("https://nid.naver.com/nidlogin.login?mode=form")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id"))).send_keys(user_id)
    driver.find_element(By.ID, "pw").send_keys(user_pw)
    driver.find_element(By.ID, "log.login").click()

# GUI 프로그램
class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("네이버 이메일 자동화")

        tk.Label(root, text="아이디").grid(row=0, column=0)
        self.entry_id = tk.Entry(root)
        self.entry_id.grid(row=0, column=1)

        tk.Label(root, text="비밀번호").grid(row=1, column=0)
        self.entry_pw = tk.Entry(root, show='*')
        self.entry_pw.grid(row=1, column=1)

        tk.Button(root, text="로그인", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(root, text="메일 등록", command=self.register_email).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="일괄 전송", command=self.bulk_send).grid(row=4, column=0, columnspan=2)

        self.driver = None

    def login(self):
        user_id = self.entry_id.get()
        user_pw = self.entry_pw.get()
        self.driver = webdriver.Chrome()
        login_to_naver(self.driver, user_id, user_pw)

    def register_email(self):
        def save():
            recipient = entry_recipient.get()
            subject = entry_subject.get()
            content = text_content.get("1.0", END).strip()
            if recipient and subject and content:
                add_email(recipient, subject, content)
                popup.destroy()

        popup = Toplevel(self.root)
        popup.title("메일 등록")

        Label(popup, text="받는사람").grid(row=0, column=0)
        entry_recipient = Entry(popup, width=40)
        entry_recipient.grid(row=0, column=1)

        Label(popup, text="제목").grid(row=1, column=0)
        entry_subject = Entry(popup, width=40)
        entry_subject.grid(row=1, column=1)

        Label(popup, text="내용").grid(row=2, column=0)
        text_content = Text(popup, width=40, height=10)
        text_content.grid(row=2, column=1)

        Button(popup, text="저장", command=save).grid(row=3, column=0, columnspan=2)

    def bulk_send(self):
        if not self.driver:
            messagebox.showerror("오류", "먼저 로그인을 해주세요.")
            return
        send_emails(self.driver)

if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()
