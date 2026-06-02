from django.db import models
from accounts.models import CustomUser,TeacherProfile


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
    
class DemoSlot(models.Model):

    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )

    date = models.DateField()

    time = models.TimeField()

    is_booked = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.teacher.username} - {self.date}"
    
class DemoBooking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
    )

    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='demo_bookings'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name='teacher_demo_bookings'
    )

    slot = models.ForeignKey(
        DemoSlot,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='confirmed'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"    