from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Course, DemoSlot,DemoBooking
from .serializers import CourseSerializer,DemoSlotSerializer,DemoBookingSerializer
from rest_framework.exceptions import NotFound


class CourseListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        courses = Course.objects.all().order_by('-created_at')

        serializer = CourseSerializer(
            courses,
            many=True
        )

        return Response(
            {
                "status": True,
                "message": "Courses fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class CourseDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:

            course = Course.objects.get(id=pk)

        except Course.DoesNotExist:

            raise NotFound("Course not found")

        serializer = CourseSerializer(course)

        return Response(
            {
                "status": True,
                "message": "Course fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
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

        return Response(serializer.data)
    
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

            return Response(
                {"error": "Invalid data"},
                status=status.HTTP_400_BAD_REQUEST
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

        return Response(
            {
                "message": "Demo Class Booked Successfully",
                "booking_id": booking.id
            },
            status=status.HTTP_201_CREATED
        )