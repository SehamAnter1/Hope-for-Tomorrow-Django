from .models import Subscribers
from rest_framework import serializers
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta :
        model=Subscribers
        fields = ['id', 'email', 'subscription_date']
        read_only_fields = ['id', 'subscription_date']   
    def validate_email(self, value):
        if Subscribers.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value

