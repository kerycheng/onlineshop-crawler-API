from django.urls import path
from crawler import views

urlpatterns = [
    path('products/', views.products),
    path('products/<str:kw>/', views.del_products),
    path('products_detail/<str:store>/<str:kw>/', views.products_detail),
]