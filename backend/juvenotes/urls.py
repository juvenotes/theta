from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

import django_js_reverse.views
from common.routes import routes as common_routes
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from mcq.api.routes import routes as mcq_routes
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.routes import routes as users_routes


router = DefaultRouter()

routes = common_routes + users_routes + mcq_routes
for route in routes:
    router.register(route["regex"], route["viewset"],
                    basename=route["basename"])

urlpatterns = [
    # path("", include("common.urls"), name="common"),
    path("", include(router.urls), name="api"),
    path("admin/", admin.site.urls, name="admin"),
    path("admin/defender/", include("defender.urls")),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    # path("api/", include(router.urls), name="api"),
    # drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls'))
]