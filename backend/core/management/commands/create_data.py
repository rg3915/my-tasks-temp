import warnings
from datetime import datetime, timedelta
from random import choice, randint

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from backend.core.utils import (
    gen_name,
    gen_phrase,
    gen_short_title,
    gen_title,
    progressbar
)
from backend.crm.models import Customer
from backend.project.models import Project
from backend.task.models import Issue, Label, Milestone, Tag, Task

fake = Faker()

warnings.filterwarnings('ignore')

REPOSITORIES = ('github/rg3915/', 'gitlab/rg3915/', 'bitbucket/rg3915/')
TAGS = ('template', 'chat', 'task', 'data', 'modelling')
LABELS = ('bug', 'frontend', 'backend', 'feature', 'refactor', 'test')
MILESTONES = ('v1.0', 'v1.5', 'v2.0', 'v3.0', 'v4.0')
STATUS = ('o', 'cl', 'ca', 'in')


def create_customers():
    for _ in progressbar(range(1, 6), 'Customers'):
        name = gen_name()
        Customer.objects.get_or_create(name=name)


def create_projects():
    for _ in progressbar(range(1, 16), 'Projects'):
        title = gen_short_title()
        customer = choice(Customer.objects.all())

        _repository_name = choice(REPOSITORIES)
        repository_name = f'{_repository_name}{slugify(title.lower())}'

        Project.objects.create(title=title, customer=customer, repository_name=repository_name)


def create_tags():
    for tag in progressbar(TAGS, 'Tags'):
        Tag.objects.get_or_create(tag=tag)


def create_labels():
    for label in progressbar(LABELS, 'Labels'):
        Label.objects.get_or_create(label=label)


def create_milestones():
    for title in progressbar(MILESTONES, 'Milestones'):
        Milestone.objects.get_or_create(title=title)


def create_issues():
    labels = Label.objects.all()
    projects = Project.objects.all()
    milestones = Milestone.objects.all()

    for issue in progressbar(range(1, 20), 'Issues'):
        data = dict(
            number=randint(1, 100),
            title=gen_title(),
            description=gen_phrase(),
            project=choice(projects),
            milestone=choice(milestones),
            status=choice(STATUS)
        )
        obj = Issue.objects.create(**data)

        for _ in range(1, 5):
            obj.labels.add(choice(labels))


def get_end_time(_start_time):
    start_time = datetime.strptime(_start_time, '%H:%M:%S').time()
    delta = timedelta(minutes=randint(15, 120))
    current_datetime = datetime.combine(datetime.today(), start_time)
    result_datetime = current_datetime + delta
    return result_datetime.time()


def create_tasks():
    projects = Project.objects.all()
    tags = Tag.objects.all()
    issues = Issue.objects.all()

    # Vamos percorrer pelas Issues porque o campo issue, em Task, é OneToOne.
    for issue in progressbar(issues, 'Tasks'):
        project = choice(projects)
        start_time = fake.time()
        data = dict(
            title=gen_title(),
            project=project,
            issue=issue,
            status=choice(STATUS),
            annotation=gen_phrase(),
            report=gen_phrase(),
            start_time=start_time,
            end_time=get_end_time(start_time),
        )
        obj = Task.objects.create(**data)

    for _ in range(1, 3):
        obj.tags.add(choice(tags))


class Command(BaseCommand):
    help = "Create data."

    def handle(self, *args, **options):
        Issue.objects.all().delete()

        create_customers()
        create_projects()
        create_tags()
        create_labels()
        create_milestones()
        create_issues()
        create_tasks()
