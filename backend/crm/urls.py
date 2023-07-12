from django.urls import include, path

from backend.crm import views as v

app_name = 'crm'

customer_patterns = [
    path('', v.customer_list, name='customer_list'),
]

urlpatterns = [
    path('', include(customer_patterns)),
]
