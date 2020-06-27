from django.urls import path

from expenses import views

urlpatterns = [
    path('create/', views.expense_form, name='create_expense'),
    path('update/<int:pk>/', views.expense_form, name='update_expense'),
    path('delete/<int:pk>/', views.delete, name='delete_expense'),
]
