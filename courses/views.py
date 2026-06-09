from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Course, DemoSlot, CourseBooking,Payment
from .serializers import CourseListSerializer,CourseDetailSerializer,DemoSlotSerializer,CourseBookingSerializer,CourseBookingDetailSerializer,PaymentSerializer
from rest_framework.exceptions import NotFound
from .utils import api_response



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
            status='confirmed'
        )

        slot.is_booked = True
        slot.save()

        return api_response(
          True,
          "Class Booked Successfully",
          {
              "booking_id": booking.id
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