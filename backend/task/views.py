from django.shortcuts import render

from .forms import IssueForm, TaskForm


def issue_list(request):
    template_name = 'crm/issue_list.html'
    context = {'form': IssueForm}
    return render(request, template_name, context)


def task_list(request):
    template_name = 'crm/task_list.html'
    context = {'form': TaskForm}
    return render(request, template_name, context)
