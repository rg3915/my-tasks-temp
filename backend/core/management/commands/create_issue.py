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

from django.core.management.base import BaseCommand

from backend.core.services import create_gitlab_issue, save_issue, save_task
from backend.project.models import Project
from backend.task.models import Milestone

warnings.filterwarnings('ignore')


def create_issue(options):
    args = dict(
        command=options['command'],
        title=options['title'],
        body=options['body'],
        labels=options['labels'],
    )
    project = Project.objects.filter(title=options['project']).first()
    args['project'] = project

    repository_name = project.get_repository_name_display()
    milestone_obj = Milestone.objects.filter(original_id=options['milestone'], project=project).first()

    # Pega o milestone correto do projeto.
    args['milestone'] = milestone_obj

    if repository_name == 'Gitlab':
        data = create_gitlab_issue(args)

    issue = save_issue(data)
    save_task(issue)


class Command(BaseCommand):
    help = 'Create issue.'

    # TODO: dá pra remover o command?

    def add_arguments(self, parser):
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')
        parser.add_argument('--command', '-c', type=str, help='start, create, end.')
        parser.add_argument('--title', '-t', type=str, help='Type the title.')
        parser.add_argument('--body', '-b', type=str, help='Type the description.')
        parser.add_argument('--labels', '-l', type=str, help='Type the labels.')
        parser.add_argument('--milestone', '-m', type=str, help='Type the milestone.')

    def handle(self, *args, **options):
        create_issue(options)
