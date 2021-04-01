import graphene
from graphene_django import DjangoObjectType
from .models import Category, Local, MenuCategory, Product, Comment

# TYPES
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "locals")

class LocalType(DjangoObjectType):
    class Meta:
        model = Local

class MenuType(DjangoObjectType):
    class Meta:
        model = MenuCategory
        fields = ("id", "local", "category", "products")

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment



# QUERIES

class CategoriesQuery(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(root, info):
        return Category.objects.all()

class LocalsQuery(graphene.ObjectType):
    all_locals = graphene.List(LocalType)

    def resolve_all_locals(root, info):
        return Local.objects.all()

class ProductsQuery(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(root, info):
        return Product.objects.all()

class CommentsQuery(graphene.ObjectType):
    all_comments = graphene.List(CommentType)

    def resolve_all_comments(root, info):
        return Comment.objects.all()


class Query(LocalsQuery, CategoriesQuery,
            ProductsQuery, CommentsQuery):
    pass


schema = graphene.Schema(query=Query)
