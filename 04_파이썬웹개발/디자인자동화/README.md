# 랜덤 상품 페이지

피그마 디자인을 기반으로 만든 랜덤 상품 페이지입니다.

## 파일 구조

```
디자인자동화/
├── index.html          # 순수 HTML 버전
├── app.py             # Flask 애플리케이션
├── templates/
│   └── index.html     # Flask 템플릿
├── requirements.txt   # Python 패키지 목록
└── README.md         # 설명서
```

## 실행 방법

### 1. 순수 HTML 버전
- `index.html` 파일을 브라우저에서 직접 열기

### 2. Flask 버전

#### 설치
```bash
pip install -r requirements.txt
```

#### 실행
```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## 기능

- **랜덤 상품 표시**: 버튼 클릭 시 랜덤한 상품 정보 표시
- **상품 정보**: 이름, 이미지, 설명, ID 표시
- **로딩 상태**: 버튼 클릭 시 로딩 애니메이션
- **에러 처리**: API 오류 시 에러 메시지 표시
- **반응형 애니메이션**: 페이드인 효과 및 호버 효과

## API 엔드포인트 (Flask 버전)

- `GET /`: 메인 페이지
- `GET /api/random-product`: 랜덤 상품 정보
- `GET /api/products`: 모든 상품 목록
- `GET /api/product/<id>`: 특정 상품 정보

## 피그마 디자인

원본 디자인: https://www.figma.com/design/LAE8xiLwnUusVjjqRBpO18/%EC%A0%9C%EB%AA%A9-%EC%97%86%EC%9D%8C?node-id=1-2

디자인 요소:
- 중앙 정렬 레이아웃
- 600px × 1024px 메인 컨테이너
- 보라색 (#7f35ff) 랜덤 버튼
- 434px × 250px 상품 이미지
- 깔끔한 타이포그래피

## 기술 스택

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask
- **이미지**: Unsplash API
- **폰트**: Inter, Noto Sans KR