from rest_framework import serializers
from .models import Vulnerability

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ['cve_id', 'description', 'severity', 'fixed']
