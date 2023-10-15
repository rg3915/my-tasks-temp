from typing import List

from ninja import Router
from ninja.orm import create_schema

from backend.task.models import Task

router = Router(tags=['Tasks'])

TaskSchema = create_schema(
    Task,
    depth=1,
    custom_fields=[
        ('customer_display', str, None),
        ('status_display', str, None),
    ],
)


@router.get('task/', response=List[TaskSchema])
def list_task(request):
    return Task.objects.all()
