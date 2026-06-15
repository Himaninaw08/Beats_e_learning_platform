from rest_framework import generics,status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,LoginSerializer,StudentProfileSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException
from beats_academy.utils import api_response  
from beats_academy.utils import custom_exception_handler 


class RegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()

    serializer_class = RegisterSerializer

    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        self.perform_create(
            serializer
        )

        return Response(
            {
                "status": True,
                "message": "Student registered successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": True,
                "message": "Login successful",
                "data": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            },
            status=status.HTTP_200_OK
        )

class StudentProfileView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = StudentProfileSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):

        return self.request.user

    def retrieve(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            self.get_object()
        )

        return Response(
            {
                "status": True,
                "message": "Profile fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop(
            'partial',
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "status": True,
                "message": "Profile updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        instance.delete()

        return Response(
            {
                "status": True,
                "message": "Profile deleted successfully",
                "data": None
            },
            status=status.HTTP_200_OK
        )