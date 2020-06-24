from django.urls import path

from customers import views

urlpatterns = [
    path('', views.index, name='customers'),
    path('<int:pk>/', views.customer, name='customer'),
    path('create/', views.customer_form, name='create_customer'),
    path('update/<int:pk>/', views.customer_form, name='update_customer'),
    path('delete/<int:pk>/', views.delete, name='delete_customer'),
]
