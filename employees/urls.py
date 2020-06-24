from django.urls import path

from employees import views

urlpatterns = [
    path('', views.index, name='employees'),
    path('<int:pk>/', views.employee, name='employee'),
    path('create/', views.employee_form, name='create_employee'),
    path('update/<int:pk>/', views.employee_form, name='update_employee'),
    path('delete/<int:pk>/', views.delete, name='delete_employee'),
]
