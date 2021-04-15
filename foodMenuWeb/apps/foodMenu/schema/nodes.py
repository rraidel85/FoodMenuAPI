from graphene import relay
from graphene_django import DjangoObjectType
from ..models import Category, Local, Product, Comment, MenuCategory

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
            'locals': ['exact'],
            'locals__name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )


class LocalNode(DjangoObjectType):
    class Meta:
        model = Local
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
            'categories': ['exact'],
            'categories__name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )


class MenuNode(DjangoObjectType):
    class Meta:
        model = MenuCategory
        filter_fields = {
            'local': ['exact'],
            'local__name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
            'category': ['exact'],
            'category__name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
            'products': ['exact'],
            'products__name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'price': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'menus': ['exact'],
            'menus__local__name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
            'menus__category__name': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

    def resolve_image(self, info):
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        filter_fields = {
            'id': ['exact'],
            'author': ['exact', 'contains', 'startswith', 'icontains', 'istartswith'],
            'comment': ['exact',],
            # 'created_at': ['iso_year__gt'],
        }
        interfaces = (relay.Node, )