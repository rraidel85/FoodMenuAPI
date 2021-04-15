from graphene import relay
from graphene_django import DjangoObjectType
from ..models import Category, Local, Product, Comment, MenuCategory

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'locals__name': ['exact'],
        }
        interfaces = (relay.Node, )


class LocalNode(DjangoObjectType):
    class Meta:
        model = Local
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'categories__name': ['exact', 'icontains'],
        }
        interfaces = (relay.Node, )


class MenuNode(DjangoObjectType):
    class Meta:
        model = MenuCategory
        filter_fields = {
            'local': ['exact'],
            'local__name': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'category__name': ['exact', 'icontains', 'istartswith'],
            'products__name': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node, )

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'price': ['exact'],
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
            'author': ['exact', 'icontains', 'istartswith'],
            'comment': ['exact'],
        }
        interfaces = (relay.Node, )