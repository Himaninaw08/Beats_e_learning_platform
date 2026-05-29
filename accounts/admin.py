from django.contrib import admin

from .models import (
    CustomUser,
    TeacherProfile
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'full_name',
        'email',
        'role',
        'is_staff',
    )

    search_fields = (
        'email',
        'full_name',
    )

    list_filter = (
        'role',
        'is_staff',
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'experience_years',
    )