from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from product.permissions import IsAuthorOrReadOnly, IsSuperUserOrReadOnly
from rest_framework.permissions import AllowAny



# Create your views here.
class PostViewSet(viewsets.GenericViewSet):
    serializer_classes = PostSerializer
    queryset = Post.objects.all()

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)        
        return Response(serializer.data)

    def retrieve(self, request, pk):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'author': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk):
        objectx = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(instance=objectx, data=request.data, context={'author': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        objectx = get_object_or_404(self.queryset, pk=pk)
        objectx.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == "create" or self.action == "update" or self.action == "destroy":
            self.permission_classes = [IsAuthorOrReadOnly | IsSuperUserOrReadOnly]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
