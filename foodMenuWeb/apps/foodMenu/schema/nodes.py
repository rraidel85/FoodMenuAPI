import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import permission_required

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

    @classmethod
    @permission_required('foodMenu.view_category')
    def get_queryset(cls, queryset, info):
        super().get_queryset(queryset, info)


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

    @classmethod
    @permission_required('foodMenu.view_local')
    def get_queryset(cls, queryset, info):
        super().get_queryset(queryset, info)

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

    full_name = graphene.String()

    def resolve_full_name(self, info):
            return f'{self.local}_{self.category}'

    @classmethod
    @permission_required('foodMenu.view_menucategory')
    def get_queryset(cls, queryset, info):
        super().get_queryset(queryset, info)

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

    @classmethod
    @permission_required('foodMenu.view_product')
    def get_queryset(cls, queryset, info):
        super().get_queryset(queryset, info)


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

    @classmethod
    @permission_required('foodMenu.view_comment')
    def get_queryset(cls, queryset, info):
        super().get_queryset(queryset, info)