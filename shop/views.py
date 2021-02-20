from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product, Category


class ProductListView(ListView):
    model = Product
    paginate_by = 12
    template_name = 'product/list.html'
    context_object_name = 'products'
    ordering = ['-updated']

    def get_queryset(self, *args, **kwargs):
        try:
            category = Category.objects.filter(slug=self.kwargs['category_slug']).first()
            products = Product.objects.filter(available=True, category=category)
        except KeyError:
            products = Product.objects.filter(available=True)
        return products
        # return products.order_by('-updated')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['category'] = self.kwargs['category_slug']
        except KeyError:
            pass
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get_queryset(self, *args, **kwargs):
        product = Product.objects.filter(slug=self.kwargs['slug'], id=self.kwargs['id'])
        return product.order_by('-updated')
