from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_doc, name='upload_doc'),
    path('list/', views.patient_list, name='patient_list'),
    path('edit/<int:pk>/', views.patient_edit, name='patient_edit'),
    path('print/<int:pk>/', views.patient_print, name='patient_print'),
]