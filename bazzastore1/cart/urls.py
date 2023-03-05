from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('reduce/<int:product_id>/', views.cart_reduce, name='cart_reduce'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]