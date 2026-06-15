from django.db import models
from accounts.models import CustomUser,TeacherProfile


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    instructor= models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'user__role': 'teacher'}
    )

    title = models.CharField(max_length=255)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    thumbnail = models.ImageField(
        upload_to='course_thumbnails/'
    )


    about_course = models.TextField()

    rating = models.DecimalField(
    max_digits=2,
    decimal_places=1,
    default=0.0
   )
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
        TeacherProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'user__role': 'teacher'}
    )

    date = models.DateField()

    time = models.TimeField()

    is_booked = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.teacher.user.email} - {self.date}"
    
class CourseBooking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
    )

    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='course_bookings'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name='teacher_course_bookings'
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
    expiry_date = models.DateField(null=True, blank=True)  

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"  

class Payment(models.Model):

    PAYMENT_METHODS = (
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('netbanking', 'Net Banking'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    booking = models.ForeignKey(
        CourseBooking,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payu_transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    payu_payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.booking.course.title} - {self.amount}"  