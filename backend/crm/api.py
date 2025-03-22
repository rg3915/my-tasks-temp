from http import HTTPStatus
from typing import List

from ninja import ModelSchema, Router
from ninja.orm import create_schema

from .models import Customer

router = Router()

CustomerSchema = create_schema(Customer, depth=1)


class CustomerSchemaIn(ModelSchema):
    class Config:
        model = Customer
        model_fields = ('name',)


@router.get('customer/', response=List[CustomerSchema], tags=['Customers'])
def list_customer(request):
    return Customer.objects.all()


@router.post('customer/', response={HTTPStatus.CREATED: CustomerSchema}, tags=['Customers'])
def create_customer(request, payload: CustomerSchemaIn):
    return Customer.objects.create(**payload.dict())
