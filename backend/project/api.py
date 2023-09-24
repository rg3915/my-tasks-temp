from http import HTTPStatus
from typing import List

from ninja import ModelSchema, Router
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


class ProjectSchemaIn(ModelSchema):
    customer_id: int = None

    class Config:
        model = Project
        model_fields = (
            'title',
            'repository_name',
            'repository_url',
        )


@router.get('project/', response=List[ProjectSchema], tags=['Projects'])
def list_project(request):
    return Project.objects.all()


@router.post('project/', response={HTTPStatus.CREATED: ProjectSchema}, tags=['Projects'])
def create_project(request, payload: ProjectSchemaIn):
    return Project.objects.create(**payload.dict())
