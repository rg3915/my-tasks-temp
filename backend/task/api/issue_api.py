from typing import List

from ninja import Router
from ninja.orm import create_schema

from backend.task.models import Issue

router = Router()

IssueSchema = create_schema(
    Issue,
    depth=1,
    custom_fields=[
        ('created_display', str, None),
        ('status_display', str, None),
        ('get_labels', str, None),
        ('get_project', str, None),
    ],)


@router.get('issue/', response=List[IssueSchema])
def list_issue(request):
    return Issue.objects.all()
