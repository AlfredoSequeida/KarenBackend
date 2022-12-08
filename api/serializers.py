from rest_framework import serializers
from karen.models import Addon


class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = ("upstream_url", "config_url", "readme_url")
