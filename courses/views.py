from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from .models import Course

from .serializers import CourseSerializer


class CourseListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        courses = Course.objects.all().order_by('-created_at')

        serializer = CourseSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)


class CourseDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:

            course = Course.objects.get(id=pk)

        except Course.DoesNotExist:

            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CourseSerializer(course)

        return Response(serializer.data)