from django.urls import path
from . import views

urlpatterns = [
    path('', views.begin, name="begin"),
    path('login/', views.log, name="login"),
    path('logout/', views.logout_view, name="login"),
    path('authenticate_user/', views.authenticate_user, name="authenticate"),
    path('add/', views.add, name="add"),
    path('get_locs/', views.get_locs),
    path('view_data/<virus>', views.getall_case, name="view_data"),
    path('add_to_db/', views.addToDb),
    path('view_data_prelim/', views.get_virus),
]