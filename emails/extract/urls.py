from django.urls import path
from extract import views

urlpatterns = [
    path('',views.extract_email,name='extract_email'),
]