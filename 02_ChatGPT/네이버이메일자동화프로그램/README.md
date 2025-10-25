# 네이버 이메일 자동화 프로그램

## 개요
이 프로그램은 네이버 메일을 자동으로 전송하는 GUI 프로그램입니다. MySQL 데이터베이스에 이메일 정보를 저장하고, 일괄전송 기능을 제공합니다.

## 기능
- 네이버 자동 로그인
- 이메일 정보 저장/수정/삭제
- 일괄 이메일 전송
- 전송 상태 관리

## 요구사항
- Python 3.13
- MySQL 데이터베이스 (database: python, user: python, password: 123456)
- Chrome 브라우저

## 필요한 라이브러리
```bash
pip install selenium mysql-connector-python webdriver-manager
```

## 데이터베이스 설정
MySQL에서 다음과 같이 설정해주세요:
```sql
CREATE DATABASE python;
CREATE USER 'python'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON python.* TO 'python'@'localhost';
FLUSH PRIVILEGES;
```

## 사용법

### 1. 프로그램 실행
```bash
python main.py
```

### 2. 네이버 로그인
- 프로그램 상단의 아이디/비밀번호 입력란에 네이버 계정 정보 입력
- "로그인" 버튼 클릭
- 크롬 브라우저가 열리며 자동으로 네이버에 로그인됩니다

### 3. 이메일 등록
- "이메일 등록" 섹션에서 받는사람, 제목, 내용 입력
- "저장" 버튼 클릭하여 데이터베이스에 저장

### 4. 이메일 관리
- **수정**: 목록에서 이메일 선택 후 내용 수정하고 "수정" 버튼 클릭
- **삭제**: 목록에서 이메일 선택 후 "삭제" 버튼 클릭
- **새로고침**: "새로고침" 버튼으로 목록 업데이트

### 5. 일괄전송
- 로그인 상태에서 "일괄전송" 버튼 클릭
- 데이터베이스의 미전송 이메일들이 순차적으로 전송됩니다
- 전송 완료된 이메일은 상태가 "완료"로 변경됩니다

## 데이터베이스 구조
```sql
CREATE TABLE email (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient VARCHAR(255) NOT NULL,    -- 받는사람 이메일
    subject VARCHAR(500) NOT NULL,      -- 제목
    content TEXT NOT NULL,              -- 내용
    status VARCHAR(50) DEFAULT '전송전'  -- 상태 (전송전/완료/실패)
);
```

## 주의사항
1. 네이버 로그인 시 2단계 인증이 설정되어 있으면 수동으로 처리해야 할 수 있습니다
2. 대량 이메일 전송 시 네이버의 스팸 정책에 주의하세요
3. 프로그램 종료 시 크롬 브라우저도 자동으로 닫힙니다
4. 네트워크 연결 상태를 확인해주세요

## 문제 해결

### 드라이버 설정 오류
**오류**: `[WinError 193] %1은(는) 올바른 Win32 응용 프로그램이 아닙니다`

**해결 방법**:
1. Chrome 브라우저가 최신 버전인지 확인
2. 다음 명령어로 라이브러리 재설치:
   ```bash
   pip uninstall selenium webdriver-manager
   pip install selenium==4.15.2 webdriver-manager==4.0.1
   ```
3. 시스템을 재시작한 후 다시 실행

### 아이디/비밀번호 인식 오류
**문제**: 네이버 로그인 시 아이디나 비밀번호가 입력되지 않는 경우

**해결된 기능**:
- JavaScript를 사용한 직접 입력 방식으로 변경
- 자동화 감지 방지 기능 추가
- 여러 선택자를 통한 요소 찾기 개선

### 이메일 전송 오류
**문제**: 메일 전송 시 요소를 찾을 수 없는 오류

**해결된 기능**:
- 다중 선택자 방식으로 요소 찾기
- iframe 처리 기능 추가
- 더 안정적인 대기 시간 설정

### 일반적인 문제들
- **데이터베이스 연결 오류**: MySQL 서비스가 실행 중인지 확인하고 계정 정보를 확인하세요
- **로그인 실패**: 네이버 계정 정보가 정확한지 확인하세요
- **이메일 전송 실패**: 네이버 로그인 상태와 네트워크 연결을 확인하세요
- **Chrome 브라우저 오류**: Chrome을 최신 버전으로 업데이트하세요

## 기술 스택
- **GUI**: tkinter
- **웹 자동화**: Selenium WebDriver
- **데이터베이스**: MySQL
- **브라우저**: Chrome

## 개발자 정보
이 프로그램은 Python 학습 목적으로 개발되었습니다.