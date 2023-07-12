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

    def get_payments(self):
        return [sprint.get_payments() for sprint in self.get_sprints()]

    def get_sprints(self):
        return self.sprints.all()

    def get_issues(self):
        return [sprint.get_issues() for sprint in self.get_sprints()]

    def get_tasks(self):
        return self.task_set.all()
