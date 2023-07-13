from django.urls import include, path

from backend.task import views as v

app_name = 'task'

issue_patterns = [
    path('', v.issue_list, name='issue_list'),
]

milestone_patterns = [
    path('', v.milestone_list, name='milestone_list'),
]

task_patterns = [
    path('', v.task_list, name='task_list'),
]

urlpatterns = [
    path('issue/', include(issue_patterns)),
    path('milestone/', include(milestone_patterns)),
    path('task/', include(task_patterns)),
]
