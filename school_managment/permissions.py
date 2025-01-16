

from rest_framework import permissions

class IsTeacherOrAdminUser(permissions.BasePermission):
    """
    Custom permission to allow access only to teachers or admin users.
    """

    def has_permission(self, request, view):
        
        return request.user.is_authenticated and (request.user.is_staff )

class IsStaffOrAdminUser(permissions.BasePermission):
    """
    Custom permission to allow access only to staff or admin users.
    """

    def has_permission(self, request, view):
        return request.user.is_owner and  request.user.is_staff  

class IsStudentOrAdminUser(permissions.BasePermission):
    """
    Custom permission to allow access only to students or admin users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.student)


 