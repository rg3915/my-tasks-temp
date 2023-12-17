from django.db import models

from backend.core.models import Active, TimeStampedModel
from backend.crm.models import Customer

REPOSITORY_NAMES = (
    ('b', 'Bitbucket'),
    ('gh', 'Github'),
    ('gl', 'Gitlab'),
)


class Project(TimeStampedModel, Active):
    title = models.CharField(max_length=255, unique=True, help_text='Digite o título do projeto')
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='cliente',
        related_name='projects',
    )
    repository_name = models.CharField(max_length=2, choices=REPOSITORY_NAMES, null=True, blank=True)
    repository_url = models.URLField(max_length=200, null=True, blank=True, help_text='Digite a url do repositório')
    gitlab_project_id = models.CharField(max_length=8, null=True, blank=True, help_text='Id do repositório no Gitlab')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return f'{self.title}'

    def repository_name_display(self):
        return self.get_repository_name_display()

    def get_payments(self):
        return [sprint.get_payments() for sprint in self.get_sprints()]

    def get_sprints(self):
        return self.sprints.all()

    def get_issues(self):
        return [sprint.get_issues() for sprint in self.get_sprints()]

    def get_tasks(self):
        from backend.task.models import Timesheet
        return Timesheet.objects.filter(task__project=self).order_by('start_time')
