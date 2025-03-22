from django.db import models

from backend.core.models import TimeStampedModel, UuidModel
from backend.task.models import Sprint


class Payment(UuidModel, TimeStampedModel):
    number = models.PositiveIntegerField()
    estimated_time = models.PositiveIntegerField(null=True, blank=True)
    estimated_value = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    value_per_hour = models.DecimalField(max_digits=7, decimal_places=2)
    spent_time_total = models.DurationField(null=True, blank=True, help_text='horas')
    value_total = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('created',)
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return f'{self.number} {self.sprint}'

    def get_spent_time_total_display(self):
        if self.spent_time_total:
            hours, remainder = divmod(self.spent_time_total.total_seconds(), 3600)
            minutes = divmod(remainder, 60)
            time_str = ''

            if hours:
                time_str += f'{int(hours)}h '

            if minutes[0]:
                time_str += f'{int(minutes[0])}m'

            if not time_str:
                return '0'

            return time_str.strip()
        return '0'
