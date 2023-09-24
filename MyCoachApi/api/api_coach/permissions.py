from rest_framework import permissions

# from profiles.models.convive import Convive
#
#
# class IsAuthenticatedConvive(permissions.BasePermission):
#     """Allows access only to authenticated convives"""
#
#     def has_permission(self, request, view):
#         return (
#             request.user and request.user.is_authenticated and type(request.user.profile) is Convive
#         )
#
#
# class CanUseTills(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user
#             and request.user.is_authenticated
#             and request.user.has_perm("core.can_use_tills")
#         )
