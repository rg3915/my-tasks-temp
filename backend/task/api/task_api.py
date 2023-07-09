from typing import List

from ninja import Router
from ninja.orm import create_schema

from backend.task.models import Task

router = Router()

TaskSchema = create_schema(Task, depth=1)


@router.get('task/', response=List[TaskSchema])
def list_task(request):
    return Task.objects.all()
