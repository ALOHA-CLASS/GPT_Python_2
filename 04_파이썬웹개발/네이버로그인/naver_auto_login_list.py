import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd

class NaverAutoLogin:
    def __init__(self):
        self.driver = None
        self.accounts_data = []
        self.current_account_index = 0
        self.setup_gui()
    
    def setup_gui(self):
        # 메인 윈도우 설정
        self.root = tk.Tk()
        self.root.title("네이버 카페 자동 댓글 작성기")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="네이버 카페 자동 댓글 작성기", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 엑셀 파일 선택
        ttk.Label(main_frame, text="엑셀 파일 선택:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50, state="readonly")
        self.file_entry.grid(row=0, column=0, padx=(0, 10))
        
        file_btn = ttk.Button(file_frame, text="파일 선택", command=self.select_excel_file)
        file_btn.grid(row=0, column=1)
        
        # 헤드리스 모드 체크박스
        self.headless_var = tk.BooleanVar()
        headless_check = ttk.Checkbutton(main_frame, text="백그라운드 실행 (헤드리스 모드)", 
                                       variable=self.headless_var)
        headless_check.grid(row=3, column=0, columnspan=2, pady=10)
        
        # 계정 목록 표시
        ttk.Label(main_frame, text="계정 목록:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        
        # 트리뷰로 계정 목록 표시
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 스크롤바 추가
        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.accounts_tree = ttk.Treeview(tree_frame, columns=("번호", "아이디", "게시글", "상태"), show="headings", height=8)
        self.accounts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 스크롤바 연결
        self.accounts_tree.config(yscrollcommand=tree_scrollbar.set)
        tree_scrollbar.config(command=self.accounts_tree.yview)
        
        # 컬럼 설정
        self.accounts_tree.heading("번호", text="번호")
        self.accounts_tree.heading("아이디", text="아이디")
        self.accounts_tree.heading("게시글", text="게시글")
        self.accounts_tree.heading("상태", text="상태")
        
        self.accounts_tree.column("번호", width=50, anchor=tk.CENTER)
        self.accounts_tree.column("아이디", width=100, anchor=tk.CENTER)
        self.accounts_tree.column("게시글", width=200, anchor=tk.CENTER)
        self.accounts_tree.column("상태", width=120, anchor=tk.CENTER)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # 순차 로그인 버튼
        sequential_btn = ttk.Button(button_frame, text="순차 로그인 및 댓글 작성 시작", 
                                  command=self.start_sequential_login, style="Accent.TButton")
        sequential_btn.grid(row=0, column=0, padx=5, ipadx=10)
        
        # 중지 버튼
        self.stop_btn = ttk.Button(button_frame, text="중지", command=self.stop_process, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5, ipadx=10)
        
        # 상태 표시
        self.status_label = ttk.Label(main_frame, text="엑셀 파일을 선택하고 '순차 로그인 및 댓글 작성 시작' 버튼을 클릭하세요.", 
                                    foreground="blue")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=10)
        
        # 닫기 버튼
        close_btn = ttk.Button(main_frame, text="종료", command=self.close_application)
        close_btn.grid(row=8, column=0, columnspan=2, pady=10)
        
        # 중지 플래그
        self.stop_flag = False
    
    def select_excel_file(self):
        """엑셀 파일 선택"""
        file_path = filedialog.askopenfilename(
            title="네이버 아이디 엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx"), ("Excel files", "*.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.load_accounts_from_excel(file_path)
    
    def load_accounts_from_excel(self, file_path):
        """엑셀 파일에서 계정 정보 로드"""
        try:
            # 엑셀 파일 읽기
            df = pd.read_excel(file_path)
            
            # 컬럼명 확인 및 정규화
            df.columns = df.columns.str.strip()
            
            # 필요한 컬럼이 있는지 확인
            required_columns = ['번호', '아이디', '비밀번호', '게시글 URL', '댓글내용']
            for col in required_columns:
                if col not in df.columns:
                    messagebox.showerror("파일 오류", f"엑셀 파일에 '{col}' 컬럼이 없습니다.\n필요한 컬럼: 번호, 아이디, 비밀번호, 게시글 URL, 댓글내용")
                    return
            
            # 계정 데이터 저장
            self.accounts_data = []
            for _, row in df.iterrows():
                if pd.notna(row['아이디']) and pd.notna(row['비밀번호']) and pd.notna(row['게시글 URL']) and pd.notna(row['댓글내용']):
                    account = {
                        'number': int(row['번호']) if pd.notna(row['번호']) else len(self.accounts_data) + 1,
                        'id': str(row['아이디']).strip(),
                        'password': str(row['비밀번호']).strip(),
                        'url': str(row['게시글 URL']).strip(),
                        'comment': str(row['댓글내용']).strip(),
                        'status': '대기'
                    }
                    self.accounts_data.append(account)
            
            # 트리뷰 업데이트
            self.update_accounts_tree()
            
            self.status_label.config(text=f"{len(self.accounts_data)}개의 계정을 로드했습니다.", foreground="green")
            
        except Exception as e:
            messagebox.showerror("파일 로드 오류", f"엑셀 파일을 읽는 중 오류가 발생했습니다:\n{str(e)}")
    
    def update_accounts_tree(self):
        """계정 목록 트리뷰 업데이트"""
        # 기존 항목 삭제
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)
        
        # 새 항목 추가
        for account in self.accounts_data:
            # URL을 짧게 표시 (도메인만)
            short_url = account.get('url', '')
            if 'cafe.naver.com' in short_url:
                cafe_name = short_url.split('/')[-2] if len(short_url.split('/')) > 1 else 'cafe'
                short_url = f"카페:{cafe_name}"
            elif len(short_url) > 30:
                short_url = short_url[:30] + "..."
            
            self.accounts_tree.insert("", "end", values=(
                account['number'], 
                account['id'], 
                short_url,
                account['status']
            ))
    
    def start_sequential_login(self):
        """순차적 로그인/로그아웃 시작"""
        if not self.accounts_data:
            messagebox.showwarning("데이터 없음", "먼저 엑셀 파일을 선택하여 계정 정보를 로드하세요.")
            return
        
        self.stop_flag = False
        self.current_account_index = 0
        self.stop_btn.config(state="normal")
        
        # 브라우저 시작
        if not self.setup_driver():
            self.stop_btn.config(state="disabled")
            return
        
        # 순차 로그인 시작
        self.process_next_account()
    
    def stop_process(self):
        """프로세스 중지"""
        self.stop_flag = True
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="프로세스가 중지되었습니다.", foreground="orange")
    
    def process_next_account(self):
        """다음 계정 처리"""
        if self.stop_flag or self.current_account_index >= len(self.accounts_data):
            self.stop_btn.config(state="disabled")
            if not self.stop_flag:
                self.status_label.config(text="모든 계정 처리가 완료되었습니다.", foreground="green")
                messagebox.showinfo("완료", "모든 계정의 로그인/로그아웃이 완료되었습니다.")
            return
        
        current_account = self.accounts_data[self.current_account_index]
        
        # 현재 계정 상태 업데이트
        current_account['status'] = '로그인 중'
        self.update_accounts_tree()
        
        self.status_label.config(text=f"계정 {current_account['number']}번 ({current_account['id']}) 로그인 중...", foreground="orange")
        self.root.update()
        
        # 로그인 시도
        if self.login_account(current_account):
            current_account['status'] = '로그인 성공'
            self.update_accounts_tree()
            self.root.update()
            
            # 게시글 URL로 이동하여 댓글 작성
            time.sleep(2)
            current_account['status'] = '댓글 작성 중'
            self.update_accounts_tree()
            self.root.update()
            
            if self.write_comment(current_account):
                current_account['status'] = '댓글 작성 완료'
            else:
                current_account['status'] = '댓글 작성 실패'
            
            self.update_accounts_tree()
            self.root.update()
            
            # 잠시 대기 후 로그아웃
            time.sleep(2)
            
            if self.logout_account():
                current_account['status'] = '로그아웃 완료'
            else:
                current_account['status'] = '로그아웃 실패'
        else:
            current_account['status'] = '로그인 실패'
        
        self.update_accounts_tree()
        self.root.update()
        
        # 다음 계정으로 이동
        self.current_account_index += 1
        
        # 1초 대기 후 다음 계정 처리
        self.root.after(1000, self.process_next_account)
    
    def login_account(self, account):
        """개별 계정 로그인"""
        try:
            # 네이버 로그인 페이지로 이동
            self.driver.get("https://nid.naver.com/nidlogin.login")
            
            wait = WebDriverWait(self.driver, 15)
            
            # 페이지가 완전히 로딩될 때까지 대기
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            time.sleep(2)
            
            # 아이디 입력
            id_field = wait.until(EC.presence_of_element_located((By.ID, "id")))
            
            # 기존 값 클리어 후 입력
            self.driver.execute_script("arguments[0].value = '';", id_field)
            time.sleep(0.5)
            
            self.driver.execute_script(f"""
                var idField = document.getElementById('id');
                idField.value = '{account['id']}';
                idField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                idField.dispatchEvent(new Event('change', {{ bubbles: true }}));
            """)
            
            time.sleep(1)
            
            # 비밀번호 입력
            pw_field = wait.until(EC.presence_of_element_located((By.ID, "pw")))
            
            # 기존 값 클리어 후 입력
            self.driver.execute_script("arguments[0].value = '';", pw_field)
            time.sleep(0.5)
            
            self.driver.execute_script(f"""
                var pwField = document.getElementById('pw');
                pwField.value = '{account['password']}';
                pwField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                pwField.dispatchEvent(new Event('change', {{ bubbles: true }}));
            """)
            
            time.sleep(1)
            
            # 로그인 버튼 클릭
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "log.login")))
            self.driver.execute_script("arguments[0].click();", login_button)
            
            # 로그인 결과 확인 (더 긴 대기 시간)
            time.sleep(5)
            
            # 추가 인증이나 보안 검사가 있는지 확인
            max_wait_time = 30  # 최대 30초 대기
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                current_url = self.driver.current_url
                
                # 로그인 성공 확인
                if "nid.naver.com/nidlogin.login" not in current_url:
                    # 추가 인증 페이지인지 확인
                    if "nid.naver.com" in current_url and ("confirm" in current_url or "auth" in current_url):
                        print("추가 인증이 필요합니다. 10초 대기 후 다시 확인합니다.")
                        time.sleep(10)
                        continue
                    else:
                        print(f"로그인 성공: {current_url}")
                        return True
                
                time.sleep(2)
            
            # 최종 URL 확인
            current_url = self.driver.current_url
            if "nid.naver.com/nidlogin.login" not in current_url:
                return True
            else:
                print(f"로그인 실패 - 최종 URL: {current_url}")
                return False
                
        except Exception as e:
            print(f"로그인 중 오류: {str(e)}")
            return False
    
    def write_comment(self, account):
        """게시글에 댓글 작성"""
        try:
            # 게시글 URL로 이동
            self.driver.get(account['url'])
            time.sleep(5)  # 페이지 로딩 대기 시간 증가
            
            wait = WebDriverWait(self.driver, 20)  # 대기 시간 증가
            
            # 페이지가 완전히 로딩될 때까지 대기
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            time.sleep(2)
            
            # 스크롤을 페이지 하단으로 이동하여 댓글창이 로딩되도록 함
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # 댓글 작성란 찾기 (여러 가능한 셀렉터 시도)
            comment_selectors = [
                ".comment_inbox_text",  # 제공된 클래스명
                "textarea[class*='comment']",
                "textarea[placeholder*='댓글']",
                ".comment_write textarea",
                "#comment_inbox_text",
                "[class*='comment_inbox']",
                "textarea[name*='comment']",
                ".se-textarea",  # 스마트 에디터
                ".comment-input textarea",
                "div[contenteditable='true']",  # contenteditable div
                "[data-testid*='comment'] textarea"
            ]
            
            comment_element = None
            for selector in comment_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            comment_element = element
                            print(f"댓글 작성란 찾음: {selector}")
                            break
                    if comment_element:
                        break
                except Exception as e:
                    print(f"셀렉터 {selector} 실패: {str(e)}")
                    continue
            
            if not comment_element:
                print("댓글 작성란을 찾을 수 없습니다. 페이지 소스 일부를 확인합니다.")
                # 디버깅을 위해 페이지 소스의 댓글 관련 부분 출력
                try:
                    page_source = self.driver.page_source
                    if "comment" in page_source.lower():
                        print("페이지에 comment 관련 요소가 있습니다.")
                    else:
                        print("페이지에 comment 관련 요소를 찾을 수 없습니다.")
                except:
                    pass
                return False
            
            # 요소가 화면에 보이도록 스크롤
            self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_element)
            time.sleep(1)
            
            # 댓글 내용 입력 (여러 방법 시도)
            try:
                # 방법 1: JavaScript querySelector로 직접 설정
                self.driver.execute_script(f"document.querySelector('.comment_inbox_text').value = '{account['comment']}';")
            except:
                try:
                    # 방법 2: 일반적인 clear와 send_keys
                    comment_element.clear()
                    comment_element.send_keys(account['comment'])
                except:
                    try:
                        # 방법 3: JavaScript로 직접 value 설정
                        self.driver.execute_script("arguments[0].value = arguments[1];", comment_element, account['comment'])
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", comment_element)
                    except:
                        try:
                            # 방법 4: contenteditable의 경우
                            self.driver.execute_script("arguments[0].innerHTML = arguments[1];", comment_element, account['comment'])
                            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", comment_element)
                        except Exception as e:
                            print(f"댓글 입력 실패: {str(e)}")
                            return False
            
            time.sleep(2)
            
            # 댓글 등록 버튼 찾기 및 클릭 (여러 가능한 셀렉터 시도)
            submit_selectors = [
                ".btn_register",  # 제공된 클래스명
                "button[class*='register']",
                "button[class*='submit']",
                ".comment_submit",
                "#comment_submit",
                "input[type='submit'][value*='등록']",
                "[class*='btn_register']",
                "button[onclick*='comment']",
                ".comment-submit",
                ".btn-comment-submit",
                "[data-testid*='submit']"
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            submit_button = element
                            print(f"등록 버튼 찾음: {selector}")
                            break
                    if submit_button:
                        break
                except Exception as e:
                    print(f"등록 버튼 셀렉터 {selector} 실패: {str(e)}")
                    continue
            
            # 텍스트 기반 검색도 시도
            if not submit_button:
                try:
                    submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '등록')] | //input[@value='등록'] | //button[contains(text(), '댓글등록')] | //button[contains(text(), '작성')]")
                    if submit_button and submit_button.is_displayed() and submit_button.is_enabled():
                        print("텍스트 기반으로 등록 버튼 찾음")
                    else:
                        submit_button = None
                except:
                    submit_button = None
            
            if not submit_button:
                print("댓글 등록 버튼을 찾을 수 없습니다.")
                return False
            
            # 등록 버튼이 화면에 보이도록 스크롤
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            
            # 댓글 등록 버튼 클릭 (여러 방법 시도)
            try:
                submit_button.click()
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", submit_button)
                except Exception as e:
                    print(f"등록 버튼 클릭 실패: {str(e)}")
                    return False
            
            time.sleep(3)  # 댓글 등록 완료 대기
            
            print(f"댓글 작성 완료: {account['comment']}")
            return True
            
        except Exception as e:
            print(f"댓글 작성 중 오류: {str(e)}")
            return False
    
    def logout_account(self):
        """로그아웃"""
        try:
            # 네이버 메인 페이지로 이동
            self.driver.get("https://www.naver.com")
            time.sleep(2)
            
            # 로그아웃 링크 찾기 및 클릭
            wait = WebDriverWait(self.driver, 10)
            
            # 다양한 로그아웃 링크 시도
            logout_selectors = [
                "a[href*='nidlogin.logout']",
                "a[href*='logout']",
                ".gnb_logout",
                "#gnb_logout_link"
            ]
            
            for selector in logout_selectors:
                try:
                    logout_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if logout_element.is_displayed():
                        logout_element.click()
                        time.sleep(2)
                        return True
                except:
                    continue
            
            # JavaScript로 로그아웃 시도
            self.driver.execute_script("location.href='https://nid.naver.com/nidlogin.logout'")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"로그아웃 중 오류: {str(e)}")
            return False
    
    def setup_driver(self):
        """웹 드라이버 설정"""
        try:
            options = Options()
            # if self.headless_var.get():
            #     options.add_argument("--headless")
            
            # 기본 옵션들
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            # WebGL 및 하드웨어 가속 관련 경고 해결
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            
            # Google API 관련 경고 해결
            options.add_argument("--disable-sync")
            options.add_argument("--disable-default-apps")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            
            # 로그 레벨 설정으로 불필요한 메시지 숨기기
            options.add_argument("--log-level=3")
            options.add_argument("--silent")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User Agent 설정
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # 자동화 감지 방지
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            
            # 자동화 감지 방지를 위한 스크립트 실행
            # self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
            
        except Exception as e:
            messagebox.showerror("드라이버 오류", f"웹 드라이버 초기화 중 오류가 발생했습니다:\n{str(e)}")
            return False
    
    def close_application(self):
        """프로그램 종료"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.root.destroy()
    
    def run(self):
        """GUI 실행"""
        # 윈도우 닫기 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)
        self.root.mainloop()


if __name__ == "__main__":
    app = NaverAutoLogin()
    app.run()