from django.db import models

# Create your models here.
class List(models.Model):
    list_name = models.CharField(max_length=255, null=False, blank=False)

class Task(models.Model):
    task_name = models.CharField(max_length=255, null=False, blank=False)
    completed = models.BooleanField(default=False, null=False)
    parent_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')

class SubTask(models.Model):
    sub_task_name = models.CharField(max_length=255, null=False, blank=False)
    completed = models.BooleanField(default=False, null=False)
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')