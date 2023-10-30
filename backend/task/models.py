from datetime import timedelta

from django.db import models

from backend.core.models import TimeStampedModel, UuidModel
from backend.core.utils import datetime_to_string
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
    color = models.CharField(max_length=7, default="#FFFFFF")

    class Meta:
        ordering = ('label',)
        verbose_name_plural = 'Labels'

    def __str__(self):
        return f'{self.label}'


class Milestone(models.Model):
    original_id = models.PositiveSmallIntegerField(help_text='Id on repository')
    title = models.CharField(max_length=30, unique=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones',
    )

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Milestones'

    def __str__(self):
        return f'{self.title}'


class Sprint(UuidModel, TimeStampedModel):
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='sprints',
    )

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Sprints'

    def __str__(self):
        return f'{self.number} - {self.project}'

    def get_issues(self):
        return self.issue_set.all()

    def get_payments(self):
        return self.payment_set.all()


STATUS = (
    ('o', 'Open'),
    ('cl', 'Close'),
    ('ca', 'Canceled'),
    ('in', 'Invalid'),
)


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

    @property
    def status_display(self):
        return self.get_status_display()

    def get_labels(self):
        return ', '.join(self.labels.values_list('label', flat=True))

    def get_project(self):
        return self.sprint.project.title


class Task(TimeStampedModel, UuidModel):
    title = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    issue = models.OneToOneField(
        Issue,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=2, choices=STATUS, default='o')
    annotation = models.TextField(null=True, blank=True)
    report = models.TextField(null=True, blank=True)
    estimate = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return f'{self.title}'

    @property
    def customer_display(self):
        return self.project.customer.name

    @property
    def status_display(self):
        return self.get_status_display()

    def get_tags(self):
        return self.tags.all()

    def get_timesheets(self):
        return self.timesheets.all()

    def last_timesheet_dict(self):
        if self.timesheets.first():
            return self.timesheets.first().to_dict()


class Timesheet(TimeStampedModel, UuidModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='timesheets',
    )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.task.issue.number} - {self.task.title}'

    @property
    def start_time_display(self):
        return datetime_to_string(self.start_time, '%H:%M')

    @property
    def start_time_display_fixed_hour(self):
        return datetime_to_string(self.start_time - timedelta(hours=3), '%H:%M')

    def get_hour(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return 0

    def to_dict(self):
        return {
            'start_time': datetime_to_string(self.start_time - timedelta(hours=3), '%H:%M'),
            'end_time': datetime_to_string(self.end_time - timedelta(hours=3), '%H:%M'),
            'get_hour': str(self.get_hour()).split('.')[0]
        }
