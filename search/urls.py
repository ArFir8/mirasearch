from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('search',views.search,name='search'),
    path('onion_redirect/', views.onion_redirect, name='onion_redirect'),         
]
