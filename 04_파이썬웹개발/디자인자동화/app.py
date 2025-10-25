from flask import Flask, render_template, jsonify
import random
import json

app = Flask(__name__)

# 랜덤 상품 데이터
products = [
    {
        "id": 1,
        "name": "맛있는 피자",
        "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=434&h=250&fit=crop",
        "description": "신선한 재료로 만든 정통 이탈리아 피자"
    },
    {
        "id": 2,
        "name": "신선한 샐러드",
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=434&h=250&fit=crop",
        "description": "건강하고 신선한 야채 샐러드"
    },
    {
        "id": 3,
        "name": "치킨 버거",
        "image": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=434&h=250&fit=crop",
        "description": "바삭한 치킨과 신선한 야채가 들어간 버거"
    },
    {
        "id": 4,
        "name": "스테이크",
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=434&h=250&fit=crop",
        "description": "완벽하게 구워진 프리미엄 스테이크"
    },
    {
        "id": 5,
        "name": "파스타",
        "image": "https://images.unsplash.com/photo-1621996346565-e3dbc353d461?w=434&h=250&fit=crop",
        "description": "이탈리아 전통 방식으로 만든 파스타"
    },
    {
        "id": 6,
        "name": "초밥",
        "image": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=434&h=250&fit=crop",
        "description": "신선한 생선으로 만든 일본식 초밥"
    },
    {
        "id": 7,
        "name": "아이스크림",
        "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=434&h=250&fit=crop",
        "description": "부드럽고 달콤한 프리미엄 아이스크림"
    },
    {
        "id": 8,
        "name": "커피",
        "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=434&h=250&fit=crop",
        "description": "신선하게 로스팅한 원두로 만든 커피"
    },
    {
        "id": 9,
        "name": "케이크",
        "image": "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=434&h=250&fit=crop",
        "description": "촉촉하고 달콤한 수제 케이크"
    },
    {
        "id": 10,
        "name": "라면",
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=434&h=250&fit=crop",
        "description": "진한 국물이 일품인 전통 라면"
    }
]

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/random-product')
def get_random_product():
    """랜덤 상품 API"""
    random_product = random.choice(products)
    return jsonify(random_product)

@app.route('/api/products')
def get_all_products():
    """모든 상품 목록 API"""
    return jsonify(products)

@app.route('/api/product/<int:product_id>')
def get_product(product_id):
    """특정 상품 조회 API"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': '상품을 찾을 수 없습니다.'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)