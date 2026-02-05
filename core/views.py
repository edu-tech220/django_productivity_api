from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from core.permissions import IsOwner
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.response import Response

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
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        tasks = Task.objects.filter(
            owner=request.user,
            status='done',
            is_active=True
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Task.objects.filter(
            owner=self.request.user,
            is_active=True
        )
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()