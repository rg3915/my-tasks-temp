from project.models import Project
from project.serializers import ProjectSerializer
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
