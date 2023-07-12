from django.shortcuts import render

from .forms import PaymentForm


def payment_list(request):
    template_name = 'financial/payment_list.html'
    context = {'form': PaymentForm}
    return render(request, template_name, context)
