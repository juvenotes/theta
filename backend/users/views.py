from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import AdditionalInfoSerializer, UserSerializer, CustomTokenObtainPairSerializer



class PersonalizationViewSet(viewsets.ModelViewSet):
    serializer_class = AdditionalInfoSerializer
    permission_classes_by_action = {'update': [IsAuthenticated]}

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'user': serializer.data,
            'message': 'User updated successfully',
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super(PersonalizationViewSet, self).get_permissions()