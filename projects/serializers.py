from rest_framework import serializers
from .models import Donation, Project,Category,ProjectImage
from rest_framework.exceptions import ValidationError
from django.db.models import Sum,F


#_______________ CategorySerializer ________________
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ='__all__'
        

#_______________ ProjectImageSerializer ________________
class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']
#_______________ ProjectSerializer ________________

class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    categories = serializers.SerializerMethodField()
    top_donors  = serializers.SerializerMethodField()
    images = ProjectImageSerializer(many=True, read_only=True) 
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
        is_detail = request and request.parser_context.get('kwargs', {}).get('pk')
        if is_detail:
            if instance.cover and 'images' in data:
                cover_data = {
                    'image': instance.cover.url,
                    'is_cover': True 
                }
                data['images'] = [cover_data] + data['images']
        else:
            data.pop('top_donors', None)
            data.pop('images', None)
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


