from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from .forms import ProductForm


def product_list(request):
    """상품 목록 조회"""
    search_query = request.GET.get('search', '')
    
    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    else:
        products = Product.objects.all()
    
    # 페이지네이션
    paginator = Paginator(products, 12)  # 페이지당 12개 상품
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': products.count(),
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    """상품 상세 조회"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


def product_create(request):
    """상품 등록"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'상품 "{product.name}"이 성공적으로 등록되었습니다.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': '상품 등록',
    }
    return render(request, 'products/product_form.html', context)


def product_update(request, pk):
    """상품 수정"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'상품 "{product.name}"이 성공적으로 수정되었습니다.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': '상품 수정',
    }
    return render(request, 'products/product_form.html', context)


def product_delete(request, pk):
    """상품 삭제"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'상품 "{product_name}"이 성공적으로 삭제되었습니다.')
        return redirect('product_list')
    
    context = {
        'product': product,
    }
    return render(request, 'products/product_confirm_delete.html', context)
