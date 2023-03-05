from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('<slug:category_slug>', views.store, name='product_list_by_category'),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
]