from django.contrib import admin
from django.urls import include, path

from .api import api

urlpatterns = [
    path('', include('backend.core.urls', namespace='core')),
    path('crm/', include('backend.crm.urls', namespace='crm')),
    path('financial/', include('backend.financial.urls', namespace='financial')),
    path('project/', include('backend.project.urls', namespace='project')),
    path('task/', include('backend.task.urls', namespace='task')),
    path('api/v1/', api.urls),
    path('admin/', admin.site.urls),
]
