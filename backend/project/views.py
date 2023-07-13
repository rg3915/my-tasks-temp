from django.shortcuts import render

from .forms import ProjectForm


def project_list(request):
    template_name = 'project/project_list.html'
    context = {'form': ProjectForm}
    return render(request, template_name, context)
