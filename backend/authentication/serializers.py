from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.contrib.auth import authenticate


class User1(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class Register(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class ChangePassword(serializers.Serializer):
    
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs


class PasswordResetRequest(serializers.Serializer):
    login_id = serializers.CharField(required=True)
    
    def validate_login_id(self, value):
        # Check if a user exists with either this username OR this email
        if not User.objects.filter(Q(username=value) | Q(email=value)).exists():
            raise serializers.ValidationError("No user found with this username or email.")
        return value


class PasswordResetConfirm(serializers.Serializer):
    login_id = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs
    
    def validate_login_id(self, value):
        # Check if user exists with username or email
        if not User.objects.filter(Q(username=value) | Q(email=value)).exists():
            raise serializers.ValidationError("No user found with this username or email.")
        return value


class Login(serializers.Serializer):
    login_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)