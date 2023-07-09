from typing import List

from ninja import Router
from ninja.orm import create_schema

from backend.task.models import Issue

router = Router()

IssueSchema = create_schema(Issue, depth=1)


@router.get('issue/', response=List[IssueSchema])
def list_issue(request):
    return Issue.objects.all()
