from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.patient_create, name='patient_create'),
    path('edit/<int:pk>/', views.patient_edit, name='patient_edit'),
    path('print/<int:pk>/', views.patient_print, name='patient_print'),
]