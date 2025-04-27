from rest_framework import serializers
from .models import Donation, Project,Category
from rest_framework.exceptions import ValidationError


#_______________ CategorySerializer ________________
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ='__all__'


#_______________ ProjectSerializer ________________
class ProjectSerializer(serializers.ModelSerializer ):
  user = serializers.ReadOnlyField(source='user.email')
  class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user', 'donations_amount', 'donations_count', 'progress', 'created_at']

#_______________ DonationSerializer ________________

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['amount', 'project_id']

