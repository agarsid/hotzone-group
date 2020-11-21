from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="index"),
    # path('search/', views.search, name="search"),
    # path('add/', views.add, name="add"),
    path('', views.begin, name="begin"),
    path('login/', views.log, name="login"),
    path('logout/', views.logout_view, name="login"),
    path('authenticate_user/', views.authenticate_user, name="authenticate"),
    path('add/', views.add, name="add")
]