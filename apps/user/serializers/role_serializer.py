from rest_framework.serializers import ModelSerializer
from apps.user.models import Role


class RoleSerializer(ModelSerializer):
    """
    角色序列化
    """

    class Meta:
        model = Role
        fields = "__all__"
        depth = 1
