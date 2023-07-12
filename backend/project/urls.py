from django.urls import include, path

from backend.project import views as v

app_name = 'project'

project_patterns = [
    path('', v.project_list, name='project_list'),
]

urlpatterns = [
    path('', include(project_patterns)),
]
