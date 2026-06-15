from django.contrib import admin
from .models import PracticeVideo, PracticeProgress, StudentPracticeUpload,Homework,HomeworkSubmission


@admin.register(PracticeVideo)
class PracticeVideoAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'title',
        'course',
        'uploaded_by',
        'duration',
        'order',
        'created_at'
    ]

    list_filter = [
        'course',
        'uploaded_by'
    ]

    search_fields = [
        'title',
        'description'
    ]

    ordering = ['order']


@admin.register(PracticeProgress)
class PracticeProgressAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'student',
        'video',
        'is_completed',
        'completed_at'
    ]

    list_filter = [
        'is_completed'
    ]

    search_fields = [
        'student__email',
        'video__title'
    ]


@admin.register(StudentPracticeUpload)
class StudentPracticeUploadAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'student',
        'video',
        'title',
        'level',
        'uploaded_at'
    ]

    list_filter = [
        'level'
    ]

    search_fields = [
        'student__email',
        'title'
    ]

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'assignment_number', 'video', 'due_date']
    list_filter = ['due_date']
    search_fields = ['title']

@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'homework', 'status', 'submitted_at']
    list_filter = ['status']
    search_fields = ['student__email', 'homework__title']