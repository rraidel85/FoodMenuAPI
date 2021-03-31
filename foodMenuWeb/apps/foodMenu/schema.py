import graphene
from graphene_django import DjangoObjectType
from .models import Category, Local, MenuCategory, Product, Comment


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "local_set")

class LocalType(DjangoObjectType):
    class Meta:
        model = Local
        fields = ("id", "name", "categories")

class MenuType(DjangoObjectType):
    class Meta:
        model = MenuCategory
        fields = ("id", "local", "product_set")

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = '__all__'

class Query(graphene.ObjectType):
    all_locals = graphene.List(LocalType)
    all_categories = graphene.List(CategoryType)

    def resolve_all_locals(root, info):
        return Local.objects.all()

    def resolve_all_categories(root, info):
        return Category.objects.all()

schema = graphene.Schema(query=Query)
