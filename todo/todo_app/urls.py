from django.urls import path
from .views import *

urlpatterns = [
    path('', AllListsView.as_view(), name='base'),
    path('<int:id>/', AListView.as_view(), name='a list'),
    path('<int:id>/tasks/', AllTasksView.as_view(), name='all tasks'),
    path('<int:id>/tasks/<int:task_id>/', ATaskView.as_view(), name='a task'),
    path('<int:id>/tasks/<int:task_id>/subtasks/', AllSubTasksView.as_view(), name='all subtasks'),
    path('<int:id>/tasks/<int:task_id>/subtasks/<int:subtask_id>/', ASubtaskView.as_view(), name='a subtask')
]