"""
https://python-gitlab.readthedocs.io/en/stable/
https://docs.gitlab.com/ee/api/issues.html

https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#update-an-issue

# Gitlab
m update_issue \
--issue=54 \
--project='my-tasks' \
--title='Editado' \
--body='The quick brown fox jumps over the lazy dog.' \
--labels='frontend,bug' \
--milestone='4287330'  # milestone.original_id

# Github
m update_issue \
--issue=1 \
--project='my-tasks-temp' \
--title='Criar issue editado' \
--body='The quick brown fox jumps over the lazy dog.' \
--labels='backend' \
--milestone='1'  # milestone.original_id
"""

import warnings

from django.core.management.base import BaseCommand

from backend.core.services import update_github_issue, update_gitlab_issue, update_issue, update_task
from backend.project.models import Project
from backend.task.models import Milestone

warnings.filterwarnings('ignore')


def update_issue_command(options):
    args = dict(
        issue=options['issue'],
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

    issue_creation_functions = {'Github': update_github_issue, 'Gitlab': update_gitlab_issue}

    if repository_name in issue_creation_functions:
        data = issue_creation_functions[repository_name](args)
    else:
        data = None

    data['project'] = project

    issue = update_issue(data)
    update_task(issue)


class Command(BaseCommand):
    help = 'Update issue.'

    def add_arguments(self, parser):
        parser.add_argument('--issue', '-i', type=str, help='Type the number of issue.')
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')
        parser.add_argument('--title', '-t', type=str, help='Type the title.')
        parser.add_argument('--body', '-b', type=str, help='Type the description.')
        parser.add_argument('--labels', '-l', type=str, help='Type the labels.')
        parser.add_argument('--milestone', '-m', type=str, help='Type the milestone.')

    def handle(self, *args, **options):
        update_issue_command(options)
