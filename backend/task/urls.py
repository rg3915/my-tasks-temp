from django.urls import include, path
from rest_framework import routers
from task.views import (
    IssueViewSet,
    LabelViewSet,
    MilestoneViewSet,
    TagViewSet,
    TaskViewSet
)

router = routers.DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'labels', LabelViewSet)
router.register(r'milestones', MilestoneViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
