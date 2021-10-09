# from rest_framework import permissions
#
#
# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         # if request.method in ['GET', 'POST', 'OPTIONS', 'HEAD']:
#         #     return True
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # Write permissions are only allowed to the owner of the snippet.
#         return obj.owner == request.user

from rest_framework import permissions

from django.conf import settings

from .utils import get_auth0_user_id_from_request


class IsCreator(permissions.BasePermission):
    """
    Object-level permission to only allow creators of an object to edit it.
    """
    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        auth0_user_id = get_auth0_user_id_from_request(request)
        print("from_auth class " + str(auth0_user_id))
        print(auth0_user_id)
        return obj.created_by == auth0_user_id

