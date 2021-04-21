import graphene
from .queries import (LocalQuery, CategoryQuery,
                      MenuQuery, ProductQuery, CommentQuery)
from .mutations import (ProductMutation, LocalMutation,
                        CategoryMutation, MenuMutation, CommentMutation)
from graphql_auth.schema import UserQuery, MeQuery
from foodMenuWeb.apps.users.schema import AuthMutation


# MAIN QUERY
class Query(LocalQuery, CategoryQuery,
            ProductQuery, MenuQuery,
            CommentQuery, UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(ProductMutation, LocalMutation,
               CategoryMutation, MenuMutation,
               CommentMutation, AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
