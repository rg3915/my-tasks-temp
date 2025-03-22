from http import HTTPStatus

from ninja import ModelSchema, Router
from ninja.orm import create_schema

from .models import Payment

router = Router(tags=['Financials'])

PaymentSchema = create_schema(Payment, custom_fields=(('get_spent_time_total_display', str, None),))


class PaymentSchemaIn(ModelSchema):
    sprint_id: int = None

    class Config:
        model = Payment
        model_fields = (
            'number',
            'estimated_time',
            'estimated_value',
            'value_per_hour',
            'spent_time_total',
            'value_total',
            'payment_date',
        )


@router.get('payment/', response=list[PaymentSchema])
def list_payment(request):
    return Payment.objects.all()


@router.post('payment/', response={HTTPStatus.CREATED: PaymentSchema})
def create_payment(request, payload: PaymentSchemaIn):
    return Payment.objects.create(**payload.dict())
