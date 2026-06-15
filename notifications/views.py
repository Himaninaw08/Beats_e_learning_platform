from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Notification
from .serializers import NotificationSerializer
from beats_academy.utils import api_response  
from beats_academy.utils import custom_exception_handler 

class MyNotificationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = NotificationSerializer(
            notifications,
            many=True
        )

        return api_response(
            True,
            "Notifications fetched successfully",
            serializer.data,
            status.HTTP_200_OK
        )
    
class MarkAsReadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        notification = Notification.objects.filter(
            id=pk,
            user=request.user
        )

        if not notification.exists():

            return api_response(
                False,
                "Notification not found",
                None,
                status.HTTP_404_NOT_FOUND
            )

        notification.update(is_read=True)

        return api_response(
            True,
            "Notification marked as read",
            None,
            status.HTTP_200_OK
        )