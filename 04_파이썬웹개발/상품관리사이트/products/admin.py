from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """상품 관리자 설정"""
    
    list_display = ['code', 'name', 'price', 'stock', 'get_stock_status', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['code', 'name', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('code', 'name', 'image')
        }),
        ('판매 정보', {
            'fields': ('price', 'stock')
        }),
        ('상세 정보', {
            'fields': ('description',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_stock_status(self, obj):
        """재고 상태 표시"""
        return obj.get_stock_status()
    get_stock_status.short_description = '재고 상태'
