from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.orm import create_schema

from backend.task.models import Issue, Project

router = Router(tags=['Issues'])

IssueSchema = create_schema(
    Issue,
    depth=1,
    custom_fields=[
        ('title_display', str, None),
        ('created_display', str, None),
        ('status_display', str, None),
        ('get_labels', str, None),
        ('get_project', str, None),
    ],
)

IssueProjectSchema = create_schema(Issue, fields=('id', 'title'))


@router.get('issue/', response=List[IssueSchema])
def list_issue(request):
    return Issue.objects.all()


@router.get('issue/{project_id}/', response=List[IssueProjectSchema])
def list_issue_by_project(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    return Issue.objects.filter(sprint__project=project)
