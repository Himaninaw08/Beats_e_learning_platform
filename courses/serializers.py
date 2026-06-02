from rest_framework import serializers
from .models import Course,DemoSlot, DemoBooking



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

class DemoSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemoSlot
        fields = '__all__'

class DemoBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemoBooking
        fields = '__all__'
        read_only_fields = ['student']