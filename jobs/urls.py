from django.urls import path

from jobs import views

urlpatterns = [
    path('create/<str:pk>/', views.job_form, name='create_job'),
    path('update/<str:pk>/', views.job1_form, name='update_job'),
    path('delete/<int:pk>/', views.delete, name='delete_job'),
]
