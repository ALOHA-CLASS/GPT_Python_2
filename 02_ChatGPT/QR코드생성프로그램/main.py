import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
import mysql.connector
import uuid
import os
from datetime import datetime

# DB 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'user': 'python',
    'password': '123456',
    'database': 'python'
}

# DB 초기화 (테이블 생성)
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS qr_code (
        no INT AUTO_INCREMENT PRIMARY KEY,
        id VARCHAR(50) NOT NULL,
        name VARCHAR(255) NOT NULL,
        value TEXT NOT NULL,
        path TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

# QR 코드 생성 함수
def create_qr_code(name, value, save_path):
    try:
        if not name or not value or not save_path:
            messagebox.showwarning('입력 오류', '모든 필드를 입력하세요.')
            return

        os.makedirs(save_path, exist_ok=True)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.png"
        file_path = os.path.join(save_path, filename)

        img = qrcode.make(value)
        img.save(file_path)

        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('INSERT INTO qr_code (id, name, value, path) VALUES (%s, %s, %s, %s)',
                    (str(uuid.uuid4()), name, value, file_path))
        conn.commit()
        conn.close()

        messagebox.showinfo('성공', f'QR 코드가 생성되었습니다:\n{file_path}')
        refresh_qr_list()
    except Exception as e:
        messagebox.showerror('오류', str(e))

# QR 코드 삭제 함수
def delete_qr(no, path):
    if messagebox.askyesno('삭제 확인', '정말 삭제하시겠습니까?'):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute('DELETE FROM qr_code WHERE no=%s', (no,))
            conn.commit()
            conn.close()

            if os.path.exists(path):
                os.remove(path)

            messagebox.showinfo('삭제 완료', 'QR 코드가 삭제되었습니다.')
            refresh_qr_list()
        except Exception as e:
            messagebox.showerror('오류', str(e))

# QR 코드 이름 수정 함수
def update_qr_name(no, new_name):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('UPDATE qr_code SET name=%s WHERE no=%s', (new_name, no))
        conn.commit()
        conn.close()
        messagebox.showinfo('수정 완료', 'QR 코드 이름이 변경되었습니다.')
        refresh_qr_list()
    except Exception as e:
        messagebox.showerror('오류', str(e))

# QR 리스트 새로고침
def refresh_qr_list():
    for row in tree.get_children():
        tree.delete(row)

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute('SELECT no, name, value, path, created_at FROM qr_code ORDER BY no DESC')
    for (no, name, value, path, created_at) in cur.fetchall():
        tree.insert('', 'end', values=(no, name, value, path, created_at))
    conn.close()

# 수정 화면 열기
def open_edit_window():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('선택 오류', '수정할 QR 코드를 선택하세요.')
        return

    item = tree.item(selected[0])
    no, name, value, path, created_at = item['values']

    edit_win = tk.Toplevel(root)
    edit_win.title('QR 코드 수정')

    tk.Label(edit_win, text='QR 코드 이름:').grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(edit_win)
    name_entry.insert(0, name)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    def save_changes():
        new_name = name_entry.get()
        if new_name:
            update_qr_name(no, new_name)
            edit_win.destroy()

    def delete_item():
        delete_qr(no, path)
        edit_win.destroy()

    tk.Button(edit_win, text='이름 수정', command=save_changes, bg='skyblue').grid(row=1, column=0, padx=10, pady=10)
    tk.Button(edit_win, text='삭제', command=delete_item, bg='tomato').grid(row=1, column=1, padx=10, pady=10)

# GUI 설정
root = tk.Tk()
root.title('QR 코드 생성 및 관리 프로그램')
root.geometry('900x600')

# 입력 프레임
frame_input = tk.LabelFrame(root, text='QR 코드 생성', padx=10, pady=10)
frame_input.pack(fill='x', padx=10, pady=10)

tk.Label(frame_input, text='QR 코드 이름:').grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_input, width=20)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text='QR 코드 값:').grid(row=0, column=2, padx=5, pady=5)
entry_value = tk.Entry(frame_input, width=40)
entry_value.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_input, text='저장 경로:').grid(row=0, column=4, padx=5, pady=5)
entry_path = tk.Entry(frame_input, width=30)
entry_path.grid(row=0, column=5, padx=5, pady=5)

def browse_path():
    folder = filedialog.askdirectory()
    if folder:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder)

tk.Button(frame_input, text='찾기', command=browse_path).grid(row=0, column=6, padx=5, pady=5)

tk.Button(frame_input, text='QR 코드 생성', command=lambda: create_qr_code(entry_name.get(), entry_value.get(), entry_path.get()), bg='lightgreen').grid(row=0, column=7, padx=10)

# 리스트 프레임
frame_list = tk.LabelFrame(root, text='QR 코드 관리 대시보드', padx=10, pady=10)
frame_list.pack(fill='both', expand=True, padx=10, pady=10)

cols = ('번호', '이름', '코드 값', '파일 경로', '등록일')
tree = ttk.Treeview(frame_list, columns=cols, show='headings')
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill='both', expand=True)

# 수정 버튼
tk.Button(root, text='선택 항목 수정/삭제', command=open_edit_window, bg='lightblue').pack(pady=10)

# 초기화
init_db()
refresh_qr_list()

root.mainloop()