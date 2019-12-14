from rest_framework import serializers
from .models import post_type_header

class post_type_headerSerializer(serializers.ModelSerializer):
    class Meta:
        model = post_type_header
        fields = ['datafields']