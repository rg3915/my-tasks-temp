'''
m create_issue \
--project='my-tasks' \
--command='create' \
--title='Criar issue' \
--body='Criar issue por linha de comando.' \
--labels='backend' \
--milestone='1'
'''
import warnings
from pprint import pprint

from django.core.management.base import BaseCommand
from faker import Faker

from backend.core.utils import make_gitlab_issue
from backend.project.models import Project
from backend.task.models import Issue, Milestone

fake = Faker()

warnings.filterwarnings('ignore')


def create_issue(options):
    args = dict(
        project=options['project'],
        command=options['command'],
        title=options['title'],
        body=options['body'],
        labels=options['labels'],
        milestone=options['milestone'],
    )
    project = Project.objects.filter(title=args['project']).first()
    args['gitlab_project_id'] = project.gitlab_project_id

    pprint(args)
    print(project.get_repository_name_display())

    repository_name = project.get_repository_name_display()
    milestone = Milestone.objects.filter(original_id=args['milestone'], project=project).first()

    # Pega o milestone correto do projeto.
    args['milestone_id'] = str(milestone.original_id)

    if repository_name == 'Gitlab':
        make_gitlab_issue(args)


class Command(BaseCommand):
    help = "Create issue."

    def add_arguments(self, parser):
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')
        parser.add_argument('--command', '-c', type=str, help='start, create, end.')
        parser.add_argument('--title', '-t', type=str, help='Type the title.')
        parser.add_argument('--body', '-b', type=str, help='Type the description.')
        parser.add_argument('--labels', '-l', type=str, help='Type the labels.')
        parser.add_argument('--milestone', '-m', type=str, help='Type the milestone.')

    def handle(self, *args, **options):
        create_issue(options)
