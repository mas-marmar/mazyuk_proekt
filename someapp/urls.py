from django.urls import path
from .views import (
    TaskListView, TaskDetailView, 
    TagListView, TagDetailView, 
    TaskTagView, TaskByTagView
)

urlpatterns = [
    path('tasks/', TaskListView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
    path('tags/', TagListView.as_view()),
    path('tags/<int:pk>/', TagDetailView.as_view()),
    path('tasks/<int:task_id>/tags/', TaskTagView.as_view()),
    path('tags/<int:tag_id>/tasks/', TaskByTagView.as_view()),
]