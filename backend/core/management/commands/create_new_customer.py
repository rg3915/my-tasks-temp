"""
novo cliente
novo projeto
novo milestone
nova sprint

m create_new_customer \
--repository_name gh \
-c ledsoft \
-p proposal-system-front \
-m psf0.8
"""
import warnings

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from backend.crm.models import Customer
from backend.project.models import Owner, Project
from backend.task.models import Milestone, Sprint


warnings.filterwarnings('ignore')


def create_customer(name):
    customer, _ = Customer.objects.get_or_create(name=name)
    return customer


def create_project(customer, project, repository_name):
    customer = Customer.objects.get(name=customer)

    repository_url = f'https://www.{repository_name}{slugify(project)}'

    repository_owner = Owner.objects.get(name='rg3915')

    title = project
    project = Project.objects.create(
        title=title,
        customer=customer,
        repository_name=repository_name,
        repository_url=repository_url,
        repository_owner=repository_owner,
    )
    return project


def create_milestone(project, original_id, title):
    project = Project.objects.get(title=project)

    Milestone.objects.get_or_create(
        original_id=original_id,
        title=title,
        project=project,
    )


def create_sprint(project):
    project = Project.objects.get(title=project)

    Sprint.objects.create(
        number=1,
        project=project,
    )


class Command(BaseCommand):
    help = "Create customer."

    def add_arguments(self, parser):
        parser.add_argument('--customer', '-c', type=str, help='Type the name of customer.')
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')
        parser.add_argument('--milestone', '-m', type=str, help='Type the milestone.')
        parser.add_argument('--repository_name', '-r', type=str, help='Type the repository name.')

    def handle(self, *args, **options):
        customer = options['customer']
        project = options['project']
        milestone = options['milestone']
        repository_name = options['repository_name']
        original_id = 1

        _customer = create_customer(name=customer)
        project = create_project(customer=_customer, project=project, repository_name=repository_name)
        create_milestone(project=project, original_id=original_id, title=milestone)
        create_sprint(project)

        print('Dados cadastrados com sucesso.')
