from django.db import models
from accounts.models import CustomUser


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    instructor= models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )

    title = models.CharField(max_length=255)

    thumbnail = models.ImageField(
        upload_to='course_thumbnails/'
    )

    description = models.TextField()

    about_course = models.TextField()

    what_you_will_learn = models.TextField()

    duration = models.CharField(max_length=100)

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES
    )

    demo_video = models.URLField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title