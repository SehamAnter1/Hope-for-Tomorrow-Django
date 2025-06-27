from rest_framework import serializers
from .models import User
class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'
    def validate_email(self, value):
        """
        Validate the email to ensure it's unique and doesn't contain spaces.
        """
        value =value.lower()
        if ' ' in value:
            raise serializers.ValidationError('Email cannot contain spaces.')

        # Check if the email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')

        return value

    def validate_password(self, value):
        """
        Custom password validation (e.g., length check).
        """
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        return value
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
