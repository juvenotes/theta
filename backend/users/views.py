from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.http import JsonResponse
from django.views.generic import RedirectView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, VerifyEmailView
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import AdditionalInfoSerializer, CustomTokenObtainPairSerializer, UserSerializer


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

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'message': 'Password reset email sent.'}, status=200)
    

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/"
    client_class = OAuth2Client 

class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"

class CustomVerifyEmailView(VerifyEmailView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return JsonResponse({'message': 'Email verified successfully'}, status=200)