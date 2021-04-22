import graphene
from django.contrib.auth.models import Group
from graphql_auth import mutations
from django.contrib.auth import get_user_model


class ManualVerify(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        username = graphene.String(required=True)

    @classmethod
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


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    # password_reset = mutations.PasswordReset.Field()    I have to make my own
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    delete_account = mutations.DeleteAccount.Field() #I have make my own for superuser can delete others accounts

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

    # my mutations
    manual_verify = ManualVerify.Field()
    add_user_to_group = AddUserToGroup.Field()
    remove_user_from_group = RemoveUserFromGroup.Field()