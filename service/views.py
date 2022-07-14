from rest_framework import generics
from .serializers import MessagesSerializer
from .models import Message
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class Messages(generics.ListAPIView):
    serializer_class = MessagesSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(from_user=self.request.user)
