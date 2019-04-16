from django.contrib import admin
from .models import Article, SuperVisor, SecurityPersonal, User
from import_export import resources


class ArticleResource(resources.ModelResource):

    class Meta:
        model = Article


admin.site.register(Article)
admin.site.register(SuperVisor)
admin.site.register(SecurityPersonal)
admin.site.register(User)
