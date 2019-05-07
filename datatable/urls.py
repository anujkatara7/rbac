from django.urls import path
from datatable import views

urlpatterns = [
    path('emp/', views.register_view, name='register_view'),
    path('django-basic-crud-create/', views.basic_crud_create_view,
         name='basic_crud_create'),
    path('django-basic-crud-list/', views.basic_crud_list_view,
         name='basic_crud_list'),
    path('django-basic-crud-delete/', views.basic_crud_del_row_view,
         name='basic_crud_delete'),
    path('<slug:slug>-<int:id>/', views.basic_crud_dynamic_public_page_view,
         name='basic_crud_dyn_pub_page'),
    path('basic_crud/<int:id>/change/', views.basic_crud_update_row_view,
         name='change_basic_crud'),
    path('basic_search_text/', views.basic_search_text_view,
         name='basic_search_text'),
    path('basic_search_dr/', views.basic_search_dr_view,
         name='basic_search_dr'),
    path('employees/', views.ContactFormView.as_view(),
         name='submit'),

]
