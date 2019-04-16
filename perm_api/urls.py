from django.urls import path, include
from perm_api.views import UserList, UserDetails, GroupList
from rest_framework.routers import DefaultRouter
from perm_api import views

router = DefaultRouter()

router.register('article', views.Articleviewset)


urlpatterns = [
    path('api/', include(router.urls)),
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
]
