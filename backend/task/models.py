from django.db import models

from backend.core.models import TimeStampedModel, UuidModel
from backend.project.models import Project


class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ('tag',)
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'{self.tag}'


class Label(models.Model):
    label = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ('label',)
        verbose_name_plural = 'Labels'

    def __str__(self):
        return f'{self.label}'


class Milestone(models.Model):
    title = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Milestones'

    def __str__(self):
        return f'{self.title}'


STATUS = (
    ('o', 'Open'),
    ('cl', 'Close'),
    ('ca', 'Canceled'),
    ('in', 'Invalid'),
)


class Sprint(UuidModel, TimeStampedModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='sprints',
    )

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Sprints'

    def __str__(self):
        return f'{self.title}'


class Issue(TimeStampedModel, UuidModel):
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
    )
    url = models.URLField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default='o')

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Issues'

    def __str__(self):
        return f'{self.number} - {self.title}'


class Task(TimeStampedModel, UuidModel):
    title = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(Tag, blank=True)
    issue = models.OneToOneField(
        Issue,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=2, choices=STATUS, default='o')
    annotation = models.TextField(null=True, blank=True)
    report = models.TextField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    estimate = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return f'{self.title}'
