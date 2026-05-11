from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import User


# ================================
# USER REGISTRATION SERIALIZER
# ================================
class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    password_confirm = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'role',
            'password',
            'password_confirm',
        )

        read_only_fields = ('id',)

    # Custom Validation
    def validate(self, attrs):

        # Password Match Check
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        return attrs

    # Create User
    def create(self, validated_data):

        # Remove confirm password
        validated_data.pop('password_confirm')

        # Create User
        user = User.objects.create_user(
            **validated_data
        )

        return user


# ================================
# USER LOGIN SERIALIZER
# ================================
class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:

            user = authenticate(
                username=email,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    "Invalid email or password."
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    "User account is disabled."
                )

            attrs['user'] = user

            return attrs

        raise serializers.ValidationError(
            "Email and password are required."
        )


# ================================
# USER PROFILE SERIALIZER
# ================================
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'role',
            'profile_image',
            'is_verified',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'email',
            'role',
            'is_verified',
            'created_at',
            'updated_at',
        )


# ================================
# STUDENT SERIALIZER
# ================================
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'profile_image',
        )

        read_only_fields = ('id', 'email')


# ================================
# TEACHER SERIALIZER
# ================================
class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'profile_image',
        )

        read_only_fields = ('id', 'email')


# ================================
# ADMIN SERIALIZER
# ================================
class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = '__all__'