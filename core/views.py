from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwner
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated ,IsOwner]

    def get_queryset(self):
        return Project.objects.filter(
        owner=self.request.user,
        is_active=True
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated ,IsOwner]

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        status = self.request.query_params.get('status')
        if status:
          queryset = queryset.filter(status=status)
        return Project.objects.filter(
        owner=self.request.user,
        is_active=True
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
