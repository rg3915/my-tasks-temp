from typing import List

from ninja import Router
from ninja.orm import create_schema

from .models import Project

router = Router()

ProjectSchema = create_schema(
    Project,
    depth=1,
    custom_fields=[
        ('repository_name_display', str, None),
    ],
    exclude=(
        'created',
        'modified',
    ))


@router.get('project/', response=List[ProjectSchema])
def list_project(request):
    return Project.objects.all()
