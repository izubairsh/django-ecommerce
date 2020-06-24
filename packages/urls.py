from django.urls import path

from packages import views

urlpatterns = [
    path('', views.index, name='packages'),
    path('create/', views.package_form, name='create_package'),
    path('update/<int:pk>/', views.package_form, name='update_package'),
    path('delete/<int:pk>/', views.delete, name='delete_package'),
]
