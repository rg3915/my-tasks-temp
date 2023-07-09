from django.shortcuts import render

from .forms import CustomerForm


def customer_list(request):
    template_name = 'crm/customer_list.html'
    context = {'form': CustomerForm}
    return render(request, template_name, context)
