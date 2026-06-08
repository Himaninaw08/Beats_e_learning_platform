from rest_framework import serializers
from .models import Course,DemoSlot, DemoBooking

class CourseSerializer(serializers.ModelSerializer):

    instructor = serializers.CharField(
        source='instructor.full_name',
        read_only=True
    )

    class Meta:

        model = Course

        fields = [
            'id',
            'title',
            'price',
            'instructor',
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

class DemoBookingDetailSerializer(serializers.ModelSerializer):

    course_title = serializers.CharField(
        source='course.title',
        read_only=True
    )

    course_price = serializers.DecimalField(
        source='course.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    teacher_name = serializers.CharField(
        source='teacher.full_name',
        read_only=True
    )

    student_name = serializers.CharField(
        source='student.full_name',
        read_only=True
    )

    student_email = serializers.EmailField(
        source='student.email',
        read_only=True
    )

    class Meta:

        model = DemoBooking

        fields = [
            'id',
            'course_title',
            'course_price',
            'teacher_name',
            'student_name',
            'student_email',
            'status',
            'created_at'
        ]