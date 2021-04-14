import graphene
from graphene_django import DjangoObjectType
from .models import Category, Local, MenuCategory, Product, Comment
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

# TYPES
class ProductType(DjangoObjectType):
    class Meta:
        model = Product

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

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {'name': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node, )

# QUERIES

class CategoriesQuery(graphene.ObjectType):
    all_categories_list = graphene.List(CategoryType)

    def resolve_all_categories_list(root, info):
        return Category.objects.all()

class LocalsQuery(graphene.ObjectType):
    all_locals = graphene.List(LocalType)
    local = graphene.Field(LocalType, id=graphene.Int(required = True))

    def resolve_all_locals(root, info):
        return Local.objects.all()

    def resolve_local(root, info, id):
        try:
            return Local.objects.get(id=id)
        except Local.DoesNotExist:
            return None

class ProductsQuery(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(root, info):
        return Product.objects.all()

class MenuQuery(graphene.ObjectType):
    all_menu = graphene.List(MenuType)

    def resolve_all_menu(root, info):
        return MenuCategory.objects.all()

class CommentsQuery(graphene.ObjectType):
    all_comments = graphene.List(CommentType)

    def resolve_all_comments(root, info):
        return Comment.objects.all()


# MAIN QUERY
class Query(LocalsQuery, CategoriesQuery,
            ProductsQuery, MenuQuery,
            CommentsQuery):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)


schema = graphene.Schema(query=Query)
