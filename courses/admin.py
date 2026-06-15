from django.contrib import admin
from .models import Course, DemoSlot, CourseBooking,Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'instructor',
        'level',
        'duration',
    )

    search_fields = ('title',)

    list_filter = ('level',)


@admin.register(DemoSlot)
class DemoSlotAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'teacher',
        'date',
        'time',
        'is_booked',
    )

    list_filter = (
        'is_booked',
        'date',
    )


@admin.register(CourseBooking)
class CourseBookingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'course',
        'teacher',
        'status',
    )

    list_filter = ('status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'booking',
        'amount',
        'payment_method',
        'status',
        'created_at'
    ]

    list_filter = [
        'status',
        'payment_method'
    ]

    search_fields = [
        'booking__student__email',
        'booking__course__title',
        'payu_transaction_id'
    ]