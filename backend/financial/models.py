from django.db import models

from backend.core.models import TimeStampedModel, UuidModel
from backend.task.models import Sprint


class Payment(UuidModel, TimeStampedModel):
    number = models.PositiveIntegerField()
    estimated_time = models.PositiveIntegerField(null=True, blank=True)
    estimated_value = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    value_per_hour = models.DecimalField(max_digits=7, decimal_places=2)
    value_total = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    hours = models.DurationField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('created',)
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"

    def __str__(self):
        return f"{self.number} {self.sprint}"
