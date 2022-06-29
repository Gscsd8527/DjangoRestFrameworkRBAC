from rest_framework import serializers
from ..models import Organization


class OrganizationSeralizer(serializers.ModelSerializer):
    """
    部门序列化
    """

    class Meta:
        model = Organization
        fields = "__all__"

