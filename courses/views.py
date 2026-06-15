from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Course, DemoSlot, CourseBooking,Payment
from .serializers import CourseListSerializer,CourseDetailSerializer,DemoSlotSerializer,CourseBookingSerializer,CourseBookingDetailSerializer,PaymentSerializer
from rest_framework.exceptions import NotFound
from beats_academy.utils import api_response  
from django.utils import timezone
from notifications.models import Notification
from beats_academy.utils import custom_exception_handler 



class CourseListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        courses = Course.objects.all().order_by('-created_at')

        serializer = CourseListSerializer(
         courses,
         many=True
)
    
        return api_response(
              True,
             "Courses fetched successfully",
              serializer.data,
              200
)


class CourseDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:

            course = Course.objects.get(id=pk)

        except Course.DoesNotExist:

            raise NotFound("Course not found")

        serializer = CourseDetailSerializer(course)

        return api_response(
              True,
              "Course fetched successfully",
              serializer.data,
              status.HTTP_200_OK
)
    
class DemoSlotListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        try:
           course = Course.objects.get(id=course_id)

        except Course.DoesNotExist:
            raise NotFound("Course not found")

        slots = DemoSlot.objects.filter(
            teacher=course.instructor,
            is_booked=False
)

        serializer = DemoSlotSerializer(
            slots,
            many=True
        )

        return api_response(
           True,
           "Slots fetched successfully",
           serializer.data,
           status.HTTP_200_OK
)
    
class BookClassView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        course_id = request.data.get('course_id')
        slot_id = request.data.get('slot_id')

        try:

            slot = DemoSlot.objects.get(
                id=slot_id,
                is_booked=False
            )

            course = Course.objects.get(
                id=course_id
            )

        except Exception:

            return api_response(
                 False,
                 "Invalid course or slot",
                 None,
                 status.HTTP_400_BAD_REQUEST
)

        booking = CourseBooking.objects.create(
            student=request.user,
            course=course,
            teacher=slot.teacher,
            slot=slot,
            status='confirmed',
            expiry_date=timezone.now().date() + timedelta(days=30)
        )

        slot.is_booked = True
        slot.save()

        return api_response(
          True,
          "Class Booked Successfully",
          {
              "booking_id": booking.id,
              "expiry_date": booking.expiry_date 
          },
          status.HTTP_201_CREATED
)
    
class CourseBookingDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):

        try:

            booking = CourseBooking.objects.get(
                id=booking_id,
                student=request.user
            )

        except CourseBooking.DoesNotExist:

            return api_response(
               False,
               "Booking not found",
               None,
               status.HTTP_404_NOT_FOUND
)
        serializer = CourseBookingDetailSerializer(
            booking
         )

        return api_response(
              True,
              "Booking details fetched successfully",
              serializer.data,
              status.HTTP_200_OK
)
    

class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        booking_id = request.data.get("booking_id")
        payment_method = request.data.get("payment_method")

        try:

            booking = CourseBooking.objects.get(
                id=booking_id,
                student=request.user
            )

        except CourseBooking.DoesNotExist:

            return api_response(
                False,
                "Booking not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        payment = Payment.objects.create(
            booking=booking,
            amount=booking.course.price,
            payment_method=payment_method,
            status='pending'
        )

        return api_response(
            True,
            "Payment created successfully",
            {
                "payment_id": payment.id,
                "amount": payment.amount
            },
            status.HTTP_201_CREATED
        )
    
class PaymentDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):

        try:

            payment = Payment.objects.get(
                id=payment_id,
                booking__student=request.user
            )

        except Payment.DoesNotExist:

            return api_response(
                False,
                "Payment not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        serializer = PaymentSerializer(payment)

        return api_response(
            True,
            "Payment details fetched successfully",
            serializer.data,
            status.HTTP_200_OK
        )
    


class BookingFeeStatusView(APIView):

    permission_classes = [IsAuthenticated]
 
    def get(self, request, booking_id):

        try:
            booking = CourseBooking.objects.get(
                id=booking_id,
                student=request.user
            )
        except CourseBooking.DoesNotExist:
            return api_response(
                False, "Booking not found", None, status.HTTP_404_NOT_FOUND
            )

        days_left = (booking.expiry_date - timezone.now().date()).days
        paid = Payment.objects.filter(booking=booking, status='success').exists()

        if 0 <= days_left <= 5 and not paid:
            already_sent = Notification.objects.filter(
                user=request.user,
                title="Fee Payment Reminder",
                created_at__date=timezone.now().date()
            ).exists()
            if not already_sent:
                Notification.objects.create(
                    user=request.user,
                    title="Fee Payment Reminder",
                    message=f"Your fee expires in {days_left} days. Amount due: ₹{booking.course.price}"
                )

        return api_response(
            True,
            "Status fetched successfully",
            {
                "days_left": days_left,
                "is_expired": days_left <= 0,
                "amount_due": booking.course.price,
                "show_popup": 0 <= days_left <= 5
            },
            status.HTTP_200_OK
        )