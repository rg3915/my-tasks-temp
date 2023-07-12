from typing import List

from ninja import Router
from ninja.orm import create_schema

from .models import Payment

router = Router()

PaymentSchema = create_schema(Payment)


@router.get('payment/', response=List[PaymentSchema])
def list_payment(request):
    return Payment.objects.all()
