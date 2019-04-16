from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='upload'),
    path('importdata/', views.import_data, name='import_data'),
    path('showtable/', views.show_table, name='show_table'),
]
