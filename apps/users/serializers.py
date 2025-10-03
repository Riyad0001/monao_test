# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()

# Signup
import uuid
from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    phone = serializers.CharField(write_only=True, allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ('first_name','last_name','email','password','password2','phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        password_validation.validate_password(attrs['password'], user=User)
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # Create user instance
        user = User(**validated_data)
        user.set_password(password)

        user.save()
        return user


# JWT Login
class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','phone','company')

# Password reset
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


from rest_framework import serializers
from django.contrib.auth import password_validation

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = self.context['request'].user

        # check old password
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        # confirm new passwords match
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Passwords do not match."})

        # validate strength
        password_validation.validate_password(attrs['new_password'], user=user)

        return attrs


from rest_framework import serializers
from .models import SendMessage

class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendMessage
        fields = ['id', 'first_name','last_name', 'email','company', 'subject', 'message', 'created_at']