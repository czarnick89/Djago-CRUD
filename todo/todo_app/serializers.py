from rest_framework import serializers
from .models import *

class SubTaskAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = "__all__"
        read_only_fields = ['parent_task']

class TaskAllSerializer(serializers.ModelSerializer):
    subtasks = SubTaskAllSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

class ListAllSerializer(serializers.ModelSerializer):
    tasks = TaskAllSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = '__all__'