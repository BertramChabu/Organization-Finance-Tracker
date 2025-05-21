from rest_framework import permissions

class IsBursar(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'bursar'
    
class IsPrincipal(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'principal'
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'
    
class IsParent(permissions.BasePermision):
    def has_permission(self,request, view):
        return request.user and request.user.is_authenticated and request.user.role =='parent'
    
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return  request.user and request.user.is_authenticated and request.user.role=='student'

