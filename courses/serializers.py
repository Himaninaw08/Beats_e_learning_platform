from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    instructor_name = serializers.CharField(
        source='instructor_name.full_name',
        read_only=True
    )

    class Meta:

        model = Course

        fields = [
            'id',
            'title',
            'instructor_name',
            'thumbnail',
            'description',
            'about_course',
            'what_you_will_learn',
            'duration',
            'level',
            'demo_video',
            'created_at',
        ]