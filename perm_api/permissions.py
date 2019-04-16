# permissions.py
from django.contrib.auth.models import Group
from rest_framework import permissions


def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required groups.
    """

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        required_groups_mapping = getattr(view, "required_groups", {})
        print(required_groups_mapping)

        # Determine the required groups for this particular request method.
        required_groups = required_groups_mapping.get(request.method, [])
        print(required_groups)

        # Return True if the user has all the required groups or is staff.
        return all([is_in_group(request.user, group_name) if group_name != "__all__" else True for group_name in required_groups]) or (request.user and request.user.is_staff)


# class IsSuperVisior(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user and request.user.groups.filter(name='Super_visior'):
#             print("Haa main hun Super_visior")
#             return True
#         return False


# class IsSecurityPersonal(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user and request.user.groups.filter(name='Security_personal'):
#             print("Haa main hun Security_personal")
#             return True
#         return False
