from django.urls import path

from orders import views

urlpatterns = [
    path('', views.orders, name="orders"),
    path('<int:pk>/', views.order, name='order'),
    path('update/<int:pk>/', views.order_form, name='create_order'),
    path('refund/<int:pk>/', views.refund_order, name='refund_order'),
    path('create/', views.order_form, name='create_order'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('get_customer/', views.get_customer, name="get_customer"),
    path('invoice/', views.invoice, name="invoice"),
    path('complete_order/', views.complete_order, name="complete_order"),

    # Transactions urls
    path('add_trans/<int:pk>/', views.add_trans, name="add_trans"),
    path('delete_trans/<int:pk>/', views.delete_trans, name='delete_trans'),

    # Items
    path('add_item/<int:pk>/', views.add_item, name="add_item"),
    path('update_item/', views.update_item, name="update_item"),
]
