from django import forms
from .models import Task, Tag

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'date', 'deadline']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']