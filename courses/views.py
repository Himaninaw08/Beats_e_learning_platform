from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Course, DemoSlot,DemoBooking
from .serializers import CourseSerializer,DemoSlotSerializer,DemoBookingSerializer,DemoBookingDetailSerializer
from rest_framework.exceptions import NotFound
from .utils import api_response



class CourseListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        courses = Course.objects.all().order_by('-created_at')

        serializer = CourseSerializer(
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

        serializer = CourseSerializer(course)

        return api_response(
              True,
              "Course fetched successfully",
              serializer.data,
              status.HTTP_200_OK
)
    
class DemoSlotListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, teacher_id):

        slots = DemoSlot.objects.filter(
            teacher_id=teacher_id,
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
    
class BookDemoClassView(APIView):

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

        booking = DemoBooking.objects.create(
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
          "Demo Class Booked Successfully",
          {
              "booking_id": booking.id
          },
          status.HTTP_201_CREATED
)
    
class DemoBookingDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):

        try:

            booking = DemoBooking.objects.get(
                id=booking_id,
                student=request.user
            )

        except DemoBooking.DoesNotExist:

            return api_response(
               False,
               "Booking not found",
               None,
               status.HTTP_404_NOT_FOUND
)
        serializer = DemoBookingDetailSerializer(
            booking
        )

        return api_response(
              True,
              "Booking details fetched successfully",
              serializer.data,
              status.HTTP_200_OK
)