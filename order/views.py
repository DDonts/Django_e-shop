from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string

from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import Cart

import pdfkit

path_wkhtmltopdf = r'D:\progs\wkhtmltopdf\bin\wkhtmltopdf.exe'


def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if len(cart) == 0:
            return redirect(reverse('shop:product_list'))
        elif form.is_valid():
            order = form.save(commit=False)  # coupon
            if cart.coupon:
                order.coupon = cart.coupon
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # launch asynchronous task

            cart.clear()

            # set the order in the session
            request.session['order_id'] = order.id
            request.session['coupon_id'] = None
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})

    pdf = pdfkit.from_string(html, False, options={'quiet': ''}, css=settings.STATIC_ROOT + 'css/pdf.css')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order_id}.pdf'
    return response
