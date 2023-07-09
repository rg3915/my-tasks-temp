from django.urls import include, path
from project.views import ProjectViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
