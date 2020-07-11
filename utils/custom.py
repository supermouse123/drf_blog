# @Time    : 2020/07/03
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination


class CustomPermission(BasePermission):
    """自定义用户操作权限类"""

    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            if request.user.is_authenticated:
                return True
            else:
                return False
        return True


class CustomPagination(PageNumberPagination):
    """自定义分页类"""

    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100