from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
