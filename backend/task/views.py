from django.shortcuts import render

from .forms import IssueForm, MilestoneForm, TaskForm


def issue_list(request):
    template_name = 'task/issue_list.html'
    context = {'form': IssueForm}
    return render(request, template_name, context)


def milestone_list(request):
    template_name = 'task/milestone_list.html'
    context = {'form': MilestoneForm}
    return render(request, template_name, context)


def task_list(request):
    template_name = 'task/task_list.html'
    context = {'form': TaskForm}
    return render(request, template_name, context)
