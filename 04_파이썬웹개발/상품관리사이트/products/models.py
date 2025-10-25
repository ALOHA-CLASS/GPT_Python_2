from django.db import models
from django.utils import timezone


class Product(models.Model):
    """상품 모델"""
    
    # 상품 이미지
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='상품 이미지'
    )
    
    # 상품 코드 (고유값)
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='상품 코드'
    )
    
    # 상품 이름
    name = models.CharField(
        max_length=200,
        verbose_name='상품명'
    )
    
    # 상품 가격
    price = models.PositiveIntegerField(
        verbose_name='가격'
    )
    
    # 재고 수량
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='재고'
    )
    
    # 상품 설명
    description = models.TextField(
        blank=True,
        verbose_name='상품 설명'
    )
    
    # 등록일
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='등록일'
    )
    
    # 수정일
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품'
        ordering = ['-created_at']  # 최신 등록순으로 정렬
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def formatted_price(self):
        """가격을 천 단위 콤마로 포맷팅"""
        return f"{self.price:,}원"
    
    def is_in_stock(self):
        """재고가 있는지 확인"""
        return self.stock > 0
    
    def get_stock_status(self):
        """재고 상태 반환"""
        if self.stock == 0:
            return "품절"
        elif self.stock <= 5:
            return "재고 부족"
        else:
            return "정상"
