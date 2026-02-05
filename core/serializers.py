from datetime import date
from rest_framework import serializers
from .models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError(
                "La fecha no puede ser pasada"
            )
        return value

    def validate_project(self, project):
        request = self.context['request']
        if project.owner != request.user:
            raise serializers.ValidationError(
                "No puedes usar proyectos de otro usuario"
            )
        return project
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']
