from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

from .models import (
    CustomUser,
    TeacherProfile
)


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:

        model = CustomUser

        fields = [
            'id',
            'full_name',
            'email',
            'password',
            'mobile_number',
            'parents_number',
            'date_of_birth',
           
        ]

    def create(self, validated_data):

        password = validated_data.pop('password')

        user = CustomUser.objects.create_user(
            password=password,
            role='student',
            **validated_data
        )

        return user



class StudentProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = [
            'id',
            'full_name',
            'email',
            'mobile_number',
            'parents_number',
            'date_of_birth',
           
        ]

        read_only_fields = [
            'id',
            'email'
        ]

class TeacherProfileSerializer(serializers.ModelSerializer):

    teacher_name = serializers.CharField(
        source='user.full_name',
        read_only=True
    )

    class Meta:

        model = TeacherProfile

        fields = [
            'id',
            'teacher_name',
            'experience_years',
            'bio',
            'profile_image',
        ]