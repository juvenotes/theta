from .views import PersonalizationViewSet


routes = [
    {"regex": r"auth/personalization", "viewset": PersonalizationViewSet, "basename": "personalization"},
]