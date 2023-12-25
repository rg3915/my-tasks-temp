'''
https://python-gitlab.readthedocs.io/en/stable/
https://docs.gitlab.com/ee/api/issues.html

https://docs.github.com/en/rest/issues?apiVersion=2022-11-28#create-an-issue

# Gitlab
m create_issue \
--project='my-tasks' \
--title='Criar issue' \
--body='Criar issue por linha de comando.' \
--labels='backend' \
--milestone='4287330'  # milestone.original_id

# Github
m create_issue \
--project='my-tasks-temp' \
--title='Criar issue 3' \
--body='Criar issue por linha de comando.' \
--labels='backend' \
--milestone='1'  # milestone.original_id
'''
import warnings

from django.core.management.base import BaseCommand

from backend.core.services import (
    create_github_issue,
    create_gitlab_issue,
    save_issue,
    save_task
)
from backend.project.models import Project
from backend.task.models import Milestone

warnings.filterwarnings('ignore')


def create_issue(options):
    args = dict(
        title=options['title'],
        body=options['body'],
        labels=options['labels'],
    )
    project = Project.objects.filter(title=options['project']).first()
    args['project'] = project

    repository_name = project.get_repository_name_display()

    # Gitlab
    milestone_obj = Milestone.objects.filter(original_id=options['milestone'], project=project).first()

    # Gitlab
    # Pega o milestone correto do projeto.
    args['milestone'] = milestone_obj

    issue_creation_functions = {
        'Github': create_github_issue,
        'Gitlab': create_gitlab_issue
    }

    if repository_name in issue_creation_functions:
        data = issue_creation_functions[repository_name](args)
    else:
        data = None

    issue = save_issue(data)
    save_task(issue)


class Command(BaseCommand):
    help = 'Create issue.'

    def add_arguments(self, parser):
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')
        parser.add_argument('--title', '-t', type=str, help='Type the title.')
        parser.add_argument('--body', '-b', type=str, help='Type the description.')
        parser.add_argument('--labels', '-l', type=str, help='Type the labels.')
        parser.add_argument('--milestone', '-m', type=str, help='Type the milestone.')

    def handle(self, *args, **options):
        create_issue(options)
