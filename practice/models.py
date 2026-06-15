from django.db import models
from django.conf import settings
from courses.models import Course


class PracticeVideo(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='practice_videos'
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_practice_videos'
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    video_file = models.FileField(
        upload_to='lesson_videos/'
    )

    duration = models.CharField(max_length=50)

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PracticeProgress(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='practice_progress'
    )

    video = models.ForeignKey(
        PracticeVideo,
        on_delete=models.CASCADE,
        related_name='progress'
    )

    is_completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('student', 'video')

    def __str__(self):
        return f"{self.student} - {self.video.title} - {self.is_completed}"


class StudentPracticeUpload(models.Model):

    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='practice_uploads'
    )

    video = models.ForeignKey(
        PracticeVideo,
        on_delete=models.CASCADE,
        related_name='student_uploads'
    )

    title = models.CharField(max_length=255)

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES
    )

    description = models.TextField()

    video_file = models.FileField(
        upload_to='practice_uploads/'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.title}"
    
class Homework(models.Model):

    
    video = models.ForeignKey(
        PracticeVideo,
        on_delete=models.CASCADE,
        related_name='homework'
    )

    title = models.CharField(max_length=255)          # "Basic Guitar Chords Practice"

    assignment_number = models.PositiveIntegerField()  # "Assignment #1"

    instructions = models.TextField()                  # "Practice C, G, D and Em chords..."

    reference_video_url = models.URLField(             # "Watch Reference Video" button
        blank=True,
        null=True
    )

    due_date = models.DateField()                      # "Due Date: 20 May 2026"

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - Assignment #{self.assignment_number}"


class HomeworkSubmission(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='homework_submissions'
    )

    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    practice_video = models.FileField(                  # student uploads practice video first
        upload_to='homework_practice_videos/',
        blank=True,
        null=True
    )

    note = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(                          # pending/submitted/approved/rejected
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    teacher_reply = models.TextField(                   # teacher's feedback/approval message
        blank=True,
        null=True
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('student', 'homework')

    def __str__(self):
        return f"{self.student} - {self.homework.title} - {self.status}"