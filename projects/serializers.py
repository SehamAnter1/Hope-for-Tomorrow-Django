from rest_framework import serializers
from .models import Donation, Project,Category
from rest_framework.exceptions import ValidationError
from django.db.models import Sum,F


#_______________ CategorySerializer ________________
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ='__all__'


#_______________ ProjectSerializer ________________
class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    categories = serializers.SerializerMethodField()
    top_donors  = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user', 'donations_amount', 'donations_count', 'progress', 'categories', 'created_at']

    def get_categories(self, obj):
        return [category.title for category in obj.categories.all()]
    def get_top_donors(self, obj):
        top_donors = (
            Donation.objects
            .filter(project=obj)
            .values('user_id', username=F('user__email'))
            .annotate(total_donated=Sum('amount'))
            .order_by('-total_donated')[:5]
        )
        return TopDonatorsSerializer(top_donors, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if not request or not request.parser_context.get('kwargs', {}).get('pk'):
            data.pop('top_donors', None)
        return data

#_______________ DonationSerializer ________________

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['amount', 'project_id']

#_______________ TopDonatorsSerializer ________________

class TopDonatorsSerializer(serializers.Serializer):
    user_id=serializers.IntegerField()
    username=serializers.CharField()
    total_donated =serializers.DecimalField(max_digits=12,decimal_places=2)
