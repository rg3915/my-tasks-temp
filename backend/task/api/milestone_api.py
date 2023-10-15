from typing import List

from ninja import Router
from ninja.orm import create_schema

from backend.task.models import Milestone

router = Router(tags=['Milestones'])

MilestoneSchema = create_schema(Milestone)


@router.get('milestone/', response=List[MilestoneSchema])
def list_milestone(request):
    return Milestone.objects.all()
