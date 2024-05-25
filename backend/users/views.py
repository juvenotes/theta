from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import AdditionalInfoSerializer, UserSerializer, CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {'create': [permissions.AllowAny]}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': serializer.data,
            'message': 'User created successfully',
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super(UserViewSet, self).get_permissions()

    @extend_schema(
        summary="User Login",
        description="This action allows a user to login",
        responses={200: CustomTokenObtainPairSerializer(many=False)}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], serializer_class=CustomTokenObtainPairSerializer)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="User Logout",
        description="This action allows a user to logout",
        responses={200: None}
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


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