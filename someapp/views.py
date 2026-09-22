from django.views import View
from django.http import JsonResponse
from json import loads
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Task, Tag, TaskTag
from .forms import TaskForm, TagForm


@method_decorator(csrf_exempt, name='dispatch')
class TaskListView(View):
    def get(self, request): #GET /tasks
        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'date': task.date,
                'deadline': task.deadline,
            })
        return JsonResponse({'data': task_list})

    def post(self, request): #POST /tasks
        raw_json = request.body
        new_data = loads(raw_json)
        form = TaskForm(new_data)

        if form.is_valid():
            task = form.save()
            return JsonResponse({'id': task.id, 'status': 'success'}, status=201)
        else:
            return JsonResponse(
                {'status': 'error', 'errors': form.errors, 'code': 400},
                status=400
            )


@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailView(View):
    def get(self, request, pk): #GET /tasks/1
        task = get_object_or_404(Task, pk=pk)
        return JsonResponse({
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'date': task.date,
            'deadline': task.deadline,
        })

    def put(self, request, pk): #PUT /tasks/1
        task = get_object_or_404(Task, pk=pk)
        raw_json = request.body
        new_data = loads(raw_json)
        form = TaskForm(new_data, instance=task)

        if form.is_valid():
            task = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Задача обновлена (полностью)',
                'data': {
                    'id': task.id,
                    'name': task.name,
                    'description': task.description,
                    'date': task.date,
                    'deadline': task.deadline,
                }
            })
        else:
            return JsonResponse(
                {'status': 'error', 'errors': form.errors, 'code': 400},
                status=400
            )

    def patch(self, request, pk): #PATCH /tasks/1
        task = get_object_or_404(Task, pk=pk)
        raw_json = request.body
        new_data = loads(raw_json)
        merged_data = model_to_dict(task)
        merged_data.update(new_data)

        form = TaskForm(merged_data, instance=task)

        if form.is_valid():
            task = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Задача обновлена (частично)',
                'data': {
                    'id': task.id,
                    'name': task.name,
                    'description': task.description,
                    'date': task.date,
                    'deadline': task.deadline,
                }
            })
        else:
            return JsonResponse(
                {'status': 'error', 'errors': form.errors, 'code': 400},
                status=400
            )


@method_decorator(csrf_exempt, name='dispatch')
class TagListView(View):
    def get(self, request): #GET /tags
        tags = Tag.objects.all()
        tag_list = [{'id': tag.id, 'name': tag.name} for tag in tags]
        return JsonResponse({'data': tag_list})

    def post(self, request): #POST /tags
        raw_json = request.body
        new_data = loads(raw_json)
        form = TagForm(new_data)

        if form.is_valid():
            tag = form.save()
            return JsonResponse({'id': tag.id, 'status': 'success'}, status=201)
        else:
            return JsonResponse(
                {'status': 'error', 'errors': form.errors, 'code': 400},
                status=400
            )


@method_decorator(csrf_exempt, name='dispatch')
class TagDetailView(View):
    def get(self, request, pk): #GET /tags/1
        tag = get_object_or_404(Tag, pk=pk)
        return JsonResponse({'id': tag.id, 'name': tag.name})

    def put(self, request, pk): #PUT /tags/1
        tag = get_object_or_404(Tag, pk=pk)
        raw_json = request.body
        new_data = loads(raw_json)
        form = TagForm(new_data, instance=tag)

        if form.is_valid():
            tag = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Тег обновлен (полностью)',
                'data': {
                    'id': tag.id,
                    'name': tag.name,
                }
            })
        else:
            return JsonResponse(
                {'status': 'error', 'errors': form.errors, 'code': 400},
                status=400
            )

    def patch(self, request, pk): #PATCH /tags/1
        tag = get_object_or_404(Tag, pk=pk)
        raw_json = request.body
        new_data = loads(raw_json)

        merged_data = model_to_dict(tag)
        merged_data.update(new_data)

        form = TagForm(merged_data, instance=tag)

        if form.is_valid():
            tag = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Тег обновлен (частично)',
                'data': {
                    'id': tag.id,
                    'name': tag.name,
                }
            })
        else:
            return JsonResponse(
                {'status': 'error', 'errors': form.errors, 'code': 400},
                status=400
            )


@method_decorator(csrf_exempt, name='dispatch')
class TaskTagView(View):
    def post(self, request, task_id): #POST /tasks/{id_задачи}/tags
        task = get_object_or_404(Task, id=task_id)
        raw_json = request.body
        new_data = loads(raw_json)

        tag_id = new_data.get('tag_id')
        if not tag_id:
            return JsonResponse({'status': 'error', 'message': 'tag_id is required', 'code': 400}, status=400)

        tag = get_object_or_404(Tag, id=tag_id)
        task_tag, created = TaskTag.objects.get_or_create(task=task, tag=tag)

        if created:
            return JsonResponse({'status': 'success', 'message': 'Тег добавлен к задаче'}, status=201)
        return JsonResponse({'status': 'error', 'message': 'Тег уже привязан', 'code': 400}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class TaskByTagView(View):
    def get(self, request, tag_id): #GET /tags/{id_тега}/tasks
        task_tags = TaskTag.objects.filter(tag_id=tag_id).select_related('task')
        task_list = []
        for tt in task_tags:
            task = tt.task
            task_list.append({
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'date': task.date,
                'deadline': task.deadline,
            })
        return JsonResponse({'data': task_list})