from rest_framework import serializers
from .models import Donation, Project
from rest_framework.exceptions import ValidationError

class ProjectSerializer(serializers.ModelSerializer ):
  user = serializers.ReadOnlyField(source='user.email')
  class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user', 'donations_amount', 'donations_count', 'progress', 'created_at']

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['amount', 'project_id']

