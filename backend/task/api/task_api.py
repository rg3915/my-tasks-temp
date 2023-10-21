from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router
from ninja.orm import create_schema

from backend.task.models import Tag, Task

router = Router(tags=['Tasks'])

TaskSchema = create_schema(
    Task,
    depth=1,
    custom_fields=[
        ('customer_display', str, None),
        ('status_display', str, None),
    ],
)


class TaskSchemaIn(ModelSchema):
    project_id: int = None
    issue_id: int = None

    class Config:
        model = Task
        model_fields = (
            'title',
            'tags',
            'annotation',
            'report',
            'start_time',
            'end_time',
            'estimate',
        )


@router.get('task/', response=list[TaskSchema])
def list_task(request):
    return Task.objects.all()


@router.post('task/', response={HTTPStatus.CREATED: TaskSchema})
def create_task(request, payload: TaskSchemaIn):
    data = payload.dict()

    tags = None
    if 'tags' in data:
        tags = data.pop('tags')

    task = Task.objects.create(**data)

    if tags:
        for pk in tags:
            tag = get_object_or_404(Tag, pk=pk)
            task.tags.add(tag)

    return task
