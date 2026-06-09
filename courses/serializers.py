from rest_framework import serializers
from .models import Course,DemoSlot, CourseBooking,Payment

class CourseListSerializer(serializers.ModelSerializer):

    instructor = serializers.CharField(
        source='instructor.full_name',
        read_only=True
    )

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'rating',
            'thumbnail',
            'instructor',
            'duration',
            'level',
            'price',
        ]

class CourseDetailSerializer(serializers.ModelSerializer):

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
            'about_course',
            'instructor',
            'duration',
            'level',
        ]

class BookClassSerializer(serializers.ModelSerializer):

    course_name = serializers.CharField(
        source='title',
        read_only=True
    )

    teacher_name = serializers.CharField(
        source='instructor.full_name',
        read_only=True
    )

    class Meta:
        model = Course
        fields = [
            'id',
            'course_name',
            'teacher_name'
        ]        

class DemoSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemoSlot
        fields = '__all__'

class CourseBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseBooking
        fields = '__all__'
        read_only_fields = ['student']

class CourseBookingDetailSerializer(serializers.ModelSerializer):

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
    booking_date = serializers.DateField(
        source='slot.date',
        read_only=True
    )

    booking_time = serializers.TimeField(
        source='slot.time',
        read_only=True
    )

    
    class Meta:
        model = CourseBooking

        fields = [
            'id',
            'course_title',
            'course_price',
            'teacher_name',
            'booking_date',
            'booking_time',
            
        ]

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            'id',
            'booking',
            'amount',
            'payment_method',
            'payu_transaction_id',
            'payu_payment_id',
            'status'
        ]