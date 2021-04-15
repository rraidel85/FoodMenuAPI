import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .nodes import CategoryNode, LocalNode, MenuNode, ProductNode, CommentNode
# from ..models import Category, Local, Product, Comment, MenuCategory


class CategoryQuery(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

class LocalQuery(graphene.ObjectType):
    local = relay.Node.Field(LocalNode)
    all_locals = DjangoFilterConnectionField(LocalNode)

class MenuQuery(graphene.ObjectType):
    all_menus = DjangoFilterConnectionField(MenuNode)

class ProductQuery(graphene.ObjectType):
    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

class CommentQuery(graphene.ObjectType):
    comment = relay.Node.Field(CommentNode)
    all_comments = DjangoFilterConnectionField(CommentNode)

