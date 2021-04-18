from django.urls import path

from products import views

urlpatterns = [
    path('', views.index, name='products'),
    path('<int:pk>/', views.product, name='product'),
    path('create/', views.product_form, name='create_product'),
    path('update/<int:pk>/', views.product_form, name='update_product'),
    path('delete/<int:pk>/', views.delete, name='delete_product')
]
