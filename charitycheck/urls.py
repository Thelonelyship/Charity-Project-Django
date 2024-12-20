from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('charitycheck/<int:charity_number>/', views.index, name='charity_by_number'),
]
