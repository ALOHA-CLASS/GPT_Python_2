# Django 상품 관리 웹사이트

## 프로젝트 개요
Django 웹 프레임워크를 사용하여 개발한 상품 관리 시스템입니다. 상품의 등록, 수정, 삭제, 조회 기능을 제공하는 완전한 CRUD 웹 애플리케이션입니다.

## 주요 기능
- ✅ **상품 등록**: 이미지, 코드, 이름, 가격, 재고, 설명 등록
- ✅ **상품 목록**: 카드 형태의 반응형 상품 목록 표시
- ✅ **상품 검색**: 상품명, 코드, 설명으로 실시간 검색
- ✅ **상품 상세 조회**: 상품의 모든 정보 상세 표시
- ✅ **상품 수정**: 기존 상품 정보 수정
- ✅ **상품 삭제**: 안전한 삭제 확인 프로세스
- ✅ **페이지네이션**: 대량 데이터 처리를 위한 페이지 분할
- ✅ **이미지 업로드**: 상품 이미지 업로드 및 미리보기
- ✅ **재고 관리**: 재고 상태 표시 (정상/부족/품절)
- ✅ **관리자 페이지**: Django Admin을 통한 백엔드 관리

## 기술 스택
- **Backend**: Django 5.2.1
- **Frontend**: HTML5, CSS3, Bootstrap 5.1.3
- **Database**: SQLite (개발용)
- **Icons**: Font Awesome 6.0
- **Image Processing**: Pillow

## 상품 데이터 구조
```python
class Product(models.Model):
    image = models.ImageField()          # 상품 이미지
    code = models.CharField()            # 상품 코드 (고유값)
    name = models.CharField()            # 상품명
    price = models.PositiveIntegerField() # 가격
    stock = models.PositiveIntegerField() # 재고
    description = models.TextField()      # 설명
    created_at = models.DateTimeField()   # 등록일
    updated_at = models.DateTimeField()   # 수정일
```

## 설치 및 실행

### 1. 필요한 라이브러리 설치
```bash
pip install django pillow
```

### 2. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 슈퍼유저 생성 (관리자 페이지 접근용)
```bash
python manage.py createsuperuser
```

### 4. 개발 서버 실행
```bash
python manage.py runserver
```

### 5. 웹사이트 접속
- **메인 페이지**: http://127.0.0.1:8000/
- **관리자 페이지**: http://127.0.0.1:8000/admin/

## 주요 URL 구조
```
/                           # 상품 목록 (홈페이지)
/product/<id>/             # 상품 상세 조회
/product/create/           # 상품 등록
/product/<id>/update/      # 상품 수정
/product/<id>/delete/      # 상품 삭제
/admin/                    # Django 관리자 페이지
```

## 디렉토리 구조
```
상품관리사이트/
├── manage.py
├── db.sqlite3
├── product_management/          # Django 프로젝트 설정
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/                    # 상품 관리 앱
│   ├── __init__.py
│   ├── admin.py                # 관리자 페이지 설정
│   ├── models.py               # 상품 모델
│   ├── views.py                # 뷰 함수들
│   ├── forms.py                # 상품 폼
│   ├── urls.py                 # URL 패턴
│   ├── migrations/             # 데이터베이스 마이그레이션
│   └── templates/products/     # HTML 템플릿
│       ├── base.html
│       ├── product_list.html
│       ├── product_detail.html
│       ├── product_form.html
│       └── product_confirm_delete.html
├── static/css/                 # 정적 파일 (CSS)
│   └── style.css
└── media/products/             # 업로드된 이미지 (자동 생성)
```

## 주요 특징

### 1. 반응형 디자인
- Bootstrap을 사용한 모바일 친화적 인터페이스
- 다양한 화면 크기에 최적화된 레이아웃

### 2. 사용자 친화적 UI/UX
- 직관적인 네비게이션
- 명확한 버튼과 아이콘
- 시각적 피드백 (호버 효과, 애니메이션)

### 3. 데이터 검증
- 폼 유효성 검사
- 중복 상품 코드 방지
- 이미지 파일 형식 검증

### 4. 검색 및 필터링
- 실시간 검색 기능
- 페이지네이션으로 성능 최적화

### 5. 이미지 처리
- 이미지 업로드 및 저장
- 이미지 미리보기 기능
- 기본 이미지 플레이스홀더

## 사용법

### 상품 등록
1. 상단 네비게이션에서 "상품 등록" 클릭
2. 상품 정보 입력 (이미지, 코드, 이름, 가격, 재고, 설명)
3. "저장" 버튼 클릭

### 상품 조회
1. 홈페이지에서 상품 목록 확인
2. 상품 카드 클릭하여 상세 정보 조회
3. 검색창을 통한 상품 검색

### 상품 수정
1. 상품 상세 페이지에서 "수정" 버튼 클릭
2. 정보 수정 후 "저장" 버튼 클릭

### 상품 삭제
1. 상품 상세 페이지에서 "삭제" 버튼 클릭
2. 삭제 확인 후 "삭제" 버튼 클릭

## 향후 개선 사항
- [ ] 상품 카테고리 기능
- [ ] 상품 리뷰 시스템
- [ ] 재고 부족 알림
- [ ] 엑셀 파일 import/export
- [ ] API 기능 추가
- [ ] 사용자 권한 관리

## 개발 환경
- Python 3.13
- Django 5.2.1
- SQLite 3
- Bootstrap 5.1.3

## 라이선스
이 프로젝트는 교육 목적으로 제작되었습니다.

## 개발자
파이썬 웹 개발 학습 프로젝트

---
*Django를 활용한 상품 관리 웹사이트 - 2024*