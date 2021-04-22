import graphene
from django.contrib.auth.models import Group
from graphql_auth import mutations
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import permission_required


# My Mutations---------------------------------------------------------------------------
class ManualVerify(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        username = graphene.String(required=True)

    @classmethod
    @permission_required('auth.change_user')
    def mutate(cls, root, info, **kwargs):
        User = get_user_model()
        username = kwargs.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return ManualVerify(success=False, errors='Wrong username')

        if user.status.verified:
            return ManualVerify(success=False, errors='User is already verified')

        user.status.verified = True
        user.status.save()
        return ManualVerify(success=True, errors=None)


class AddUserToGroup(graphene.Mutation):

    success = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        group = graphene.String(required=True)

    @classmethod
    @permission_required('auth.change_user')
    def mutate(cls, root, info, **kwargs):
        User = get_user_model()
        username = kwargs.get('username')
        group = kwargs.get('group')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return AddUserToGroup(success=False, errors='Wrong username')
        try:
            group = Group.objects.get(name=group)
        except Group.DoesNotExist:
            return AddUserToGroup(success=False, errors='Wrong group name')

        try:
            user.groups.add(group)
        except Exception as e:
            return AddUserToGroup(success=False, errors=str(e))

        return AddUserToGroup(success=True, errors=None)


class RemoveUserFromGroup(graphene.Mutation):

    success = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        group = graphene.String(required=True)

    @classmethod
    @permission_required('auth.change_user')
    def mutate(cls, root, info, **kwargs):
        User = get_user_model()
        username = kwargs.get('username')
        group = kwargs.get('group')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return RemoveUserFromGroup(success=False, errors='Wrong username')
        try:
            group = Group.objects.get(name=group)
        except Group.DoesNotExist:
            return RemoveUserFromGroup(success=False, errors='Wrong group name')

        try:
            user.groups.remove(group)
        except Exception as e:
            return RemoveUserFromGroup(success=False, errors=str(e))

        return RemoveUserFromGroup(success=True, errors=None)

class MyRegister(mutations.Register, graphene.Mutation):
    @classmethod
    @permission_required('auth.add_user')
    def mutate(cls, root, info, **input):
        return super().mutate(root, info, **input)



# Auth Mutations--------------------------------------------------
class AuthMutation(graphene.ObjectType):
    register = MyRegister.Field() # need administrador permissions
    # password_reset = mutations.PasswordReset.Field()   # I have to make my own password_reset mutation

    # Need to be authenticated
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    delete_account = mutations.DeleteAccount.Field() #I have make my own for superuser can delete others accounts

    # django-graphql-jwt inheritances  # No need of being authenticated
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

    # my mutations
    manual_verify = ManualVerify.Field(description='Apply this after register mutation to verify a user')
    add_user_to_group = AddUserToGroup.Field(description='After a user is created use this to add it to a group')
    remove_user_from_group = RemoveUserFromGroup.Field(description='Remove user from a group')