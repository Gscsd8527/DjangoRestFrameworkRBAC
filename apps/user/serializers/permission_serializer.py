from rest_framework import serializers
from apps.user.models import Permission


class PermissionSeralizer(serializers.ModelSerializer):
    """
    权限序列化
    """

    class Meta:
        model = Permission
        fields = "__all__"