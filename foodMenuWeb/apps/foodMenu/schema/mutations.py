import graphene
from graphene import relay
from graphql_jwt.decorators import permission_required
from graphql_relay import from_global_id
from graphene_file_upload.scalars import Upload
from graphene.types import Decimal
from .nodes import CategoryNode, LocalNode, MenuNode, ProductNode, CommentNode
from ..models import Category, Local, Product, Comment, MenuCategory


# Products Mutations--------------------------------------------------
class CreateProduct(relay.ClientIDMutation):
    """Create a new product"""
    class Input:
        name = graphene.String(required=True)
        description = graphene.String()
        price = Decimal()
        image = Upload()

    product = graphene.Field(ProductNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.add_product')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            image = data.pop("image")
        except KeyError:
            image = None

        try:
            product = Product.objects.create(**data)
            if image:
                product.image = image
                product.save()
        except Exception as e:
            return CreateProduct(product=None, success=False, error=str(e))

        return CreateProduct(product=product,success=True,error=None)



class UpdateProduct(relay.ClientIDMutation):
    """Update a product by ID"""
    class Input:
        id = graphene.String(required=True)
        name = graphene.String()
        description = graphene.String()
        price = Decimal()
        image = Upload()

    product = graphene.Field(ProductNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.change_product')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            image = data.pop("image")
        except KeyError:
            image = None

        try:
            pk = from_global_id(data['id'])[1]
            del data['id']
            Product.objects.filter(pk=pk).update(**data)
            product = Product.objects.get(pk=pk)
            if image:
                product.image = image
                product.save()
        except Exception as e:
            return UpdateProduct(product=None, success=False, error=str(e))

        return UpdateProduct(product=product, success=True, error=None)


class DeleteProducts(relay.ClientIDMutation):
    """Delete a list or a single product by ID"""
    class Input:
        products = graphene.List(graphene.String, required=True)

    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.delete_product')
    def mutate_and_get_payload(cls, root, info, products):
        try:
            for node_id in products:
                pk = from_global_id(node_id)[1]
                product = Product.objects.get(pk=pk)
                product.delete()
        except Exception as e:
            return DeleteProducts(success=False,error=str(e))

        return DeleteProducts(success=True, error=None)

class ProductMutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_products = DeleteProducts.Field()



# Local Mutations--------------------------------------------
class CreateLocal(relay.ClientIDMutation):
    """Create a new local"""
    class Input:
        name = graphene.String(required=True)

    local = graphene.Field(LocalNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.add_local')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            local = Local.objects.create(**data)
        except Exception as e:
            return CreateLocal(local=None, success=False, error=str(e))

        return CreateLocal(local=local,success=True,error=None)


class UpdateLocal(relay.ClientIDMutation):
    """Update a local by ID"""
    class Input:
        id = graphene.String(required=True)
        name = graphene.String()
        # categories = graphene.List(graphene.String)

    local = graphene.Field(LocalNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.change_local')
    def mutate_and_get_payload(cls, root, info, **data):

        # try:
        #     categories = data.pop("categories")
        # except KeyError:
        #     categories = None

        try:
            local_pk = from_global_id(data['id'])[1]
            del data['id']
            Local.objects.filter(pk=local_pk).update(**data)
            local = Local.objects.get(pk=local_pk)
        except Exception as e:
            return UpdateLocal(local=None, success=False, error=str(e))

        return UpdateLocal(local=local, success=True, error=None)



class DeleteLocals(relay.ClientIDMutation):
    """Delete a list or a single local by ID"""
    class Input:
        locals = graphene.List(graphene.String, required=True)

    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.delete_local')
    def mutate_and_get_payload(cls, root, info, locals):
        try:
            for node_id in locals:
                pk = from_global_id(node_id)[1]
                local = Local.objects.get(pk=pk)
                local.delete()
        except Exception as e:
            return DeleteLocals(success=False,error=str(e))

        return DeleteLocals(success=True, error=None)


class LocalMutation(graphene.ObjectType):
    create_local = CreateLocal.Field()
    update_local = UpdateLocal.Field()
    delete_locals = DeleteLocals.Field()



# Category Mutations--------------------------------------------

class CreateCategory(relay.ClientIDMutation):
    """Create a new category"""
    class Input:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.add_category')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            category = Category.objects.create(**data)
        except Exception as e:
            return CreateCategory(category=None, success=False, error=str(e))

        return CreateCategory(category=category,success=True,error=None)


class UpdateCategory(relay.ClientIDMutation):
    """Update a category by ID"""
    class Input:
        id = graphene.String(required=True)
        name = graphene.String()

    category = graphene.Field(CategoryNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.change_category')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            category_pk = from_global_id(data['id'])[1]
            del data['id']
            Category.objects.filter(pk=category_pk).update(**data)
            category = Category.objects.get(pk=category_pk)
        except Exception as e:
            return UpdateCategory(category=None, success=False, error=str(e))

        return UpdateCategory(category=category, success=True, error=None)



class DeleteCategories(relay.ClientIDMutation):
    """Delete a list or a single category by ID"""
    class Input:
        categories = graphene.List(graphene.String, required=True)

    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.delete_category')
    def mutate_and_get_payload(cls, root, info, categories):
        try:
            for node_id in categories:
                pk = from_global_id(node_id)[1]
                category = Category.objects.get(pk=pk)
                category.delete()
        except Exception as e:
            return DeleteCategories(success=False,error=str(e))

        return DeleteCategories(success=True, error=None)


class CategoryMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_categories = DeleteCategories.Field()




# Menus Mutations--------------------------------------------

class CreateMenu(relay.ClientIDMutation):
    """Create a new local and category relationship (menu)"""
    class Input:
        local = graphene.String(required=True)
        category = graphene.String(required=True)
        products = graphene.List(graphene.String)

    menu = graphene.Field(MenuNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.add_menucategory')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            products = data.pop("products")
        except KeyError:
            products = None

        try:
            local_id = from_global_id(data['local'])[1]
            local = Local.objects.get(id=local_id)
            category_id = from_global_id(data['category'])[1]
            category = Category.objects.get(id=category_id)
            menu = MenuCategory.objects.create(local=local, category=category)
            if products:
                for node_id in products:
                    product_pk = from_global_id(node_id)[1]
                    menu.products.add(product_pk)
        except Exception as e:
            return CreateMenu(menu=None, success=False, error=str(e))

        return CreateMenu(menu=menu, success=True, error=None)


class AddProductsToMenu(relay.ClientIDMutation):
    """Add products to a local and category relationship (menu)"""
    class Input:
        local = graphene.String(required=True)
        category = graphene.String(required=True)
        products = graphene.List(graphene.String, required=True)

    menu = graphene.Field(MenuNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.change_menucategory')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            local = from_global_id(data['local'])[1]
            category = from_global_id(data['category'])[1]
            menu = MenuCategory.objects.get(local=local, category=category)
            for node_id in data['products']:
                product_pk = from_global_id(node_id)[1]
                menu.products.add(product_pk)
        except Exception as e:
            return AddProductsToMenu(menu=None, success=False, error=str(e))

        return AddProductsToMenu(menu=menu, success=True, error=None)



class DeleteProductsFromMenu(relay.ClientIDMutation):
    """Delete products from a local and category relationship (menu)"""
    class Input:
        local = graphene.String(required=True)
        category = graphene.String(required=True)
        products = graphene.List(graphene.String, required=True)

    menu = graphene.Field(MenuNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.change_menucategory')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            local = from_global_id(data['local'])[1]
            category = from_global_id(data['category'])[1]
            menu = MenuCategory.objects.get(local=local, category=category)
            for node_id in data['products']:
                product_pk = from_global_id(node_id)[1]
                menu.products.remove(product_pk)
        except Exception as e:
            return DeleteProductsFromMenu(menu=None, success=False, error=str(e))

        return DeleteProductsFromMenu(menu=menu, success=True, error=None)



class DeleteMenu(relay.ClientIDMutation):
    """Delete a single local and category relationship (menu)"""
    class Input:
        local = graphene.String(required=True)
        category = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.delete_menucategory')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            local = from_global_id(data['local'])[1]
            category = from_global_id(data['category'])[1]
            menu = MenuCategory.objects.get(local=local, category=category)
            menu.delete()
        except Exception as e:
            return DeleteMenu(success=False,error=str(e))

        return DeleteMenu(success=True, error=None)


class MenuMutation(graphene.ObjectType):
    create_menu = CreateMenu.Field()
    add_products_to_menu = AddProductsToMenu.Field()
    delete_products_from_menu = DeleteProductsFromMenu.Field()
    delete_menu = DeleteMenu.Field()




# Comment Mutations--------------------------------------------

class CreateComment(relay.ClientIDMutation):
    """Create a new comment"""
    class Input:
        author = graphene.String(required=True)
        comment = graphene.String(required=True)

    comment = graphene.Field(CommentNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.add_comment')
    def mutate_and_get_payload(cls, root, info, **data):
        try:
            comment = Comment.objects.create(**data)
        except Exception as e:
            return CreateComment(comment=None, success=False, error=str(e))

        return CreateComment(comment=comment,success=True,error=None)


class DeleteComments(relay.ClientIDMutation):
    """Delete a list or a single comment by ID"""
    class Input:
        comments = graphene.List(graphene.String, required=True)

    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @permission_required('foodMenu.delete_comment')
    def mutate_and_get_payload(cls, root, info, comments):
        try:
            for node_id in comments:
                pk = from_global_id(node_id)[1]
                comment = Comment.objects.get(pk=pk)
                comment.delete()
        except Exception as e:
            return DeleteComments(success=False,error=str(e))

        return DeleteComments(success=True, error=None)


class CommentMutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    delete_comments = DeleteComments.Field()