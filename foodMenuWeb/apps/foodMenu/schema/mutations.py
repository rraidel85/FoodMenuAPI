import graphene
from graphene import relay
from graphql_relay import from_global_id
from graphene_file_upload.scalars import Upload
from graphene.types import Decimal
from .nodes import CategoryNode, LocalNode, MenuNode, ProductNode, CommentNode
from ..models import Category, Local, Product, Comment, MenuCategory



class CreateProduct(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        menus = graphene.List(graphene.ID)
        description = graphene.String()
        price = Decimal()
        image = Upload()

    product = graphene.Field(ProductNode)
    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        """Create a new product"""
        try:
            image = data.pop("image")
        except KeyError:
            image = None

        try:
            menus = data.pop("menus")
        except KeyError:
            menus = None

        try:
            product = Product.objects.create(**data)
            if image:
                product.image = image
            if menus:
                for node_id in menus:
                    pk = from_global_id(node_id)[1]
                    product.menus.add(pk)
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
        pk = from_global_id(data['id'])[1]
        del data['id']

        try:
            image = data.pop("image")
        except KeyError:
            image = None

        try:
            menus = data.pop("menus")
        except KeyError:
            menus = None

        try:
            Product.objects.filter(pk=pk).update(**data)
            product = Product.objects.get(pk=pk)
            if image or menus:
                if image:
                    product.image = image
                if menus:
                    for node_id in menus:
                        pk = from_global_id(node_id)[1]
                        product.menus.add(pk)
                product.save()
            return UpdateProduct(product=product, success=True, error=None)
        except Exception as e:
            return UpdateProduct(product=None, success=False, error=str(e))


class DeleteProduct(relay.ClientIDMutation):
    class Input:
        id = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        try:
            pk = from_global_id(id)[1]
            product = Product.objects.get(pk=pk)
            product.delete()
            return DeleteProduct(success=True, error=None)
        except Exception as e:
            return DeleteProduct(success=False,error=str(e))

class ProductMutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()