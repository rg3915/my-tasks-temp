from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router
from ninja.orm import create_schema

from backend.core.management.commands.start_task import start_task_command
from backend.core.management.commands.stop_task import stop_task_command
from backend.task.models import Tag, Task

router = Router(tags=['Tasks'])

TaskSchema = create_schema(
    Task,
    depth=1,
    custom_fields=[
        ('title_display', str, None),
        ('customer_display', str, None),
        ('status_display', str, None),
        ('last_timesheet_dict', dict, None),
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


@router.patch('task/{slug}/', response=TaskSchema)
def update_task(request, slug: str, payload: TaskSchemaIn):
    instance = get_object_or_404(Task, slug=slug)
    data = payload.dict()

    tags = None
    if 'tags' in data:
        tags = data.pop('tags')

        for pk in tags:
            tag = get_object_or_404(Tag, pk=pk)
            instance.tags.add(tag)

    for attr, value in data.items():
        setattr(instance, attr, value)

    instance.save()
    return instance


@router.get('task/{slug}/start/')
def start_task_api(request, slug: str, previous_hour: bool):
    task = get_object_or_404(Task, slug=slug)

    options = dict(
        project=task.project.title,
        task=task.issue.number,
        previous_hour=previous_hour,
    )

    status, previous_hour, timesheet = start_task_command(options)

    if previous_hour:
        start_time = timesheet.start_time_display_fixed_hour
    else:
        start_time = timesheet.start_time_display

    return {'start_time': start_time, 'success': status}


@router.get('task/{slug}/stop/')
def stop_task_api(request, slug: str):
    task = get_object_or_404(Task, slug=slug)

    options = dict(
        project=task.project.title,
        task=task.issue.number,
    )

    response = stop_task_command(options)

    return {'success': response}
