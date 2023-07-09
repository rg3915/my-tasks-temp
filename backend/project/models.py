from django.db import models

from backend.core.models import Active, TimeStampedModel
from backend.crm.models import Customer


class Project(TimeStampedModel, Active):
    title = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='cliente',
        related_name='projects',
    )
    repository_name = models.CharField(max_length=100, null=True, blank=True)
    repository_url = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return f'{self.title}'
