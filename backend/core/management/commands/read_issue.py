'''
https://python-gitlab.readthedocs.io/en/stable/
https://docs.gitlab.com/ee/api/issues.html

https://docs.github.com/en/rest/issues?apiVersion=2022-11-28#create-an-issue

# Gitlab
m read_issue \
--project='my-tasks' \
--milestone='4287330' \
--assignee='rg3915'

# Github
m read_issue \
--project='my-tasks-temp' \
--milestone='1' \
--assignee='rg3915'
'''
import warnings

from django.core.management.base import BaseCommand

from backend.core.services import (
    read_github_issue,
    read_gitlab_issue,
    save_issue_multiple,
    save_task_multiple
)
from backend.project.models import Project
from backend.task.models import Milestone

warnings.filterwarnings('ignore')


def read_issue(options):
    args = dict(
        milestone=options['milestone'],
        assignee=options['assignee'],
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
        'Github': read_github_issue,
        'Gitlab': read_gitlab_issue
    }

    if repository_name in issue_creation_functions:
        data = issue_creation_functions[repository_name](args)
    else:
        data = None

    issues = save_issue_multiple(data)
    save_task_multiple(issues)


class Command(BaseCommand):
    help = 'Read issue.'

    def add_arguments(self, parser):
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')
        parser.add_argument('--assignee', '-a', type=str, default='rg3915', help='Type the assignee.')
        parser.add_argument('--milestone', '-m', type=str, help='Type the milestone.')

    def handle(self, *args, **options):
        read_issue(options)
