from django.contrib import admin
from .models import Course, DemoSlot, DemoBooking


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


@admin.register(DemoBooking)
class DemoBookingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'course',
        'teacher',
        'status',
    )

    list_filter = ('status',)