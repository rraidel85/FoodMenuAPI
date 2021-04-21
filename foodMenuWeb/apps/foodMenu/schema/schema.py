import graphene
from .queries import (LocalQuery, CategoryQuery,
                      MenuQuery, ProductQuery, CommentQuery)
from .mutations import (ProductMutation, LocalMutation,
                        CategoryMutation, MenuMutation, CommentMutation)

# MAIN QUERY
class Query(LocalQuery, CategoryQuery,
            ProductQuery, MenuQuery,
            CommentQuery, graphene.ObjectType):
    pass

class Mutation(ProductMutation, LocalMutation,
               CategoryMutation, MenuMutation,
               CommentMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
