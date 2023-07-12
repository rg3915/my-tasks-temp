from django.urls import include, path

from backend.financial import views as v

app_name = 'financial'

payment_patterns = [
    path('', v.payment_list, name='payment_list'),
]

urlpatterns = [
    path('', include(payment_patterns)),
]
