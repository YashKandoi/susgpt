from .models import Website
from rest_framework import serializers

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'company_name', 'url', 'output']


