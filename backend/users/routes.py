from .views import PersonalizationViewSet, UserViewSet


routes = [
    {"regex": r"users", "viewset": UserViewSet, "basename": "user"},
    {"regex": r"users/personalization", "viewset": PersonalizationViewSet, "basename": "personalization"},
]