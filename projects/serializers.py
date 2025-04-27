from rest_framework import serializers

from .models import Project

class ProjectSerializer(serializers.ModelSerializer ):
  class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user', 'donations_amount', 'donations_count', 'progress', 'created_at']
