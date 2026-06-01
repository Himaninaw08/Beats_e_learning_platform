from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from .serializers import StudentProfileSerializer
from .models import CustomUser





class RegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()

    serializer_class = RegisterSerializer

    permission_classes = [AllowAny]

class StudentProfileView( generics.RetrieveUpdateDestroyAPIView):

    serializer_class = StudentProfileSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):

        return self.request.user 


