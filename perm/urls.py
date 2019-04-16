from django.urls import path
from . import views
# from django.contrib.auth.views import LoginView
# app_name = "perm"

urlpatterns = [
    path('', views.my_view, name='view'),
    # path('login/', LoginView.as_view(template_name='users/login.html'), name="login"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
