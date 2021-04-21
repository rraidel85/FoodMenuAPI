import graphene
from graphene import relay
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
    def mutate_and_get_payload(cls, root, info, locals):
        try:
            for node_id in locals:
                pk = from_global_id(node_id)[1]
                locals = Local.objects.get(pk=pk)
                locals.delete()
        except Exception as e:
            return DeleteLocals(success=False,error=str(e))

        return DeleteLocals(success=True, error=None)


class LocalMutation(graphene.ObjectType):
    create_local = CreateLocal.Field()
    update_local = UpdateLocal.Field()
    delete_locals = DeleteLocals.Field()