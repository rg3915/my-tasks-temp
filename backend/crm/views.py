from crm.models import Customer
from crm.serializers import CustomerSerializer
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
