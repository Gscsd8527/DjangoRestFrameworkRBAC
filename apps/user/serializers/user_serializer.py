from rest_framework import serializers
from ..models import User
from ..serializers.organization_serializer import OrganizationSeralizer


class UserInfoListSerializer(serializers.ModelSerializer):
    """
    用户信息表
    """
    # department = OrganizationSeralizer()
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'mobile', 'email', 'position', 'department')

        # depth = 1

