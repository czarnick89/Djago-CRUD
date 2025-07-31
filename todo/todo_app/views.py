from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.
class AllListsView(APIView):
    
    def get(self, request): 
        lists = List.objects.all()
        serialized_lists = ListAllSerializer(lists, many=True)
        return Response(serialized_lists.data, status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ListAllSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AListView(APIView):

    def fetch_list(self, id):
        if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
            return get_object_or_404(List, id=int(id))
        else:
            return get_object_or_404(List, list_name__iexact=id)
        
    def get(self, request, id):
        list = self.fetch_list(id)
        serializer = ListAllSerializer(list)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, id):
        list = self.fetch_list(id)
        serializer = ListAllSerializer(list, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        list = self.fetch_list(id)
        list.delete()
        return Response({"message": "Student deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class AllTasksView(APIView):

    def get(self, request, id):
        list_obj = get_object_or_404(List, id=id)
        tasks = list_obj.tasks.all()
        serializer = TaskAllSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        list_obj = get_object_or_404(List, id=id)
        data = request.data.copy()
        data['parent_list'] = list_obj.id

        serializer = TaskAllSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ATaskView(APIView):

    def get(self, request, id, task_id):
        list_obj = get_object_or_404(List, id=id)
        task = get_object_or_404(Task, id=task_id, parent_list=list_obj)
        serializer = TaskAllSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id, task_id):
    
        list_obj = get_object_or_404(List, id=id)
        task = get_object_or_404(Task, id=task_id, parent_list=list_obj)
        data = {
            "task_name": request.data.get("task_name", task.task_name),
            "completed": request.data.get("completed", task.completed),
        }

        serializer = TaskAllSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, task_id):
        list_obj = get_object_or_404(List, id=id)
        task = get_object_or_404(Task, id=task_id, parent_list=list_obj)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AllSubTasksView(APIView):

    def get(self, request, id, task_id):
        list_obj = get_object_or_404(List, id=id)
        task = get_object_or_404(Task, id=task_id, parent_list=list_obj)
        subtasks = SubTask.objects.filter(parent_task=task)
        serializer = SubTaskAllSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, task_id):
        list_obj = get_object_or_404(List, id=id)
        task = get_object_or_404(Task, id=task_id, parent_list=list_obj)
        serializer = SubTaskAllSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent_task=task)

            if task.completed:
                task.completed = False
                task.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ASubtaskView(APIView):
    def get(self, request, id, task_id, subtask_id):
        list_obj = get_object_or_404(List, id=id)
        task = get_object_or_404(Task, id=task_id, parent_list=list_obj)
        subtask = get_object_or_404(SubTask, id=subtask_id, parent_task=task)

        serializer = SubTaskAllSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, task_id, subtask_id):
        list_obj = get_object_or_404(List, id=id)
        task = get_object_or_404(Task, id=task_id, parent_list=list_obj)
        subtask = get_object_or_404(SubTask, id=subtask_id, parent_task=task)

        serializer = SubTaskAllSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if task.subtask_set.filter(completed=False).count() == 0:
                task.completed = True
                task.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, task_id, subtask_id):
        list_obj = get_object_or_404(List, id=id)
        task = get_object_or_404(Task, id=task_id, parent_list=list_obj)
        subtask = get_object_or_404(SubTask, id=subtask_id, parent_task=task)

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    