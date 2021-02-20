from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.models import Product


@require_POST
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    form = CartAddProductForm(request.POST)
    cd = {}
    if form.is_valid():
        cd = form.cleaned_data
    else:
        cd['quantity'] = 1
        cd['override'] = False
    cart.add(product=product,
             quantity=cd['quantity'],
             override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                                'quantity': item['quantity'],
                                'override': True
                            })
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form})
