from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    # path('<slug:category_slug>/', views.product_list_view, name='product_list_by_slug'),
    path('<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_slug'),
    # path('<int:id>/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    # path('', views.product_list_view, name='product_list'),

    path('', views.ProductListView.as_view(), name='product_list'),
]
