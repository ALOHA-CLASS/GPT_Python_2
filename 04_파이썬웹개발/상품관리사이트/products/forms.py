from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """상품 폼"""
    
    class Meta:
        model = Product
        fields = ['image', 'code', 'name', 'price', 'stock', 'description']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '상품 코드를 입력하세요'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '상품명을 입력하세요'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '가격을 입력하세요',
                'min': '0'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '재고 수량을 입력하세요',
                'min': '0'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '상품 설명을 입력하세요',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 필수 필드에 required 표시
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
                field.label = f"{field.label} *"
    
    def clean_code(self):
        """상품 코드 유효성 검증"""
        code = self.cleaned_data.get('code')
        if code:
            code = code.strip().upper()
            # 기존 상품과 중복 체크 (수정 시 본인 제외)
            existing_product = Product.objects.filter(code=code)
            if self.instance.pk:
                existing_product = existing_product.exclude(pk=self.instance.pk)
            
            if existing_product.exists():
                raise forms.ValidationError('이미 존재하는 상품 코드입니다.')
        
        return code
    
    def clean_price(self):
        """가격 유효성 검증"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('가격은 0 이상이어야 합니다.')
        return price
    
    def clean_stock(self):
        """재고 유효성 검증"""
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('재고는 0 이상이어야 합니다.')
        return stock