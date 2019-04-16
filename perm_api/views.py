# from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User, Group
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, \
    TokenHasScope
from .serializer import UserSerializer, GroupSerializer, ArticleSerializer
from perm.models import Article
from .permissions import HasGroupPermission
# Create your views here.


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class Articleviewset(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['Super_visior'],
        'PUT': ['Security_personal'],
    }
    # def get_permissions(self):
    #     if self.request.method == 'POST' or self.request.method == 'DELETE':
    #         self.permission_classes = [IsSuperVisior]
    #     return super(Articleviewset, self).get_permissions()
