from rest_framework import generics, permissions
from django_filters import rest_framework as filters 

from .models import Category, Publication
from .serializers import CategorySerializers, PublicationSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import CategoryFilter, PublicationFilter


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CategoryFilter

    serializer_class = CategorySerializers
    queryset = Category.objects.all()

class PublicationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.filter(is_archived=False)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PublicationFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PublicationRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
