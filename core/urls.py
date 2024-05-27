# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('upload/', views.upload_view, name='upload'),
    path('query-builder/', views.query_builder_view, name='query_builder'),
]
