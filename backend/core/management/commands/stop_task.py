'''
m stop_task --project='my-tasks' --task=1
'''
import warnings
import subprocess
from django.core.management.base import BaseCommand
from rich import print
from rich.console import Console

from backend.core.services import remove_aqui_from_tarefas, stop_timesheet, write_x_on_tarefas
from backend.project.models import Project
from backend.task.models import Task

console = Console()

warnings.filterwarnings('ignore')


def stop_task_command(options) -> bool:
    # get project
    project = Project.objects.filter(title=options['project']).first()

    # A Task está diretamente relacionada com a Issue.
    # get task
    task = Task.objects.filter(
        project=project,
        issue__number=options['task']
    ).first()

    # Fecha a Task
    task.status = 'cl'
    task.save()

    # Fecha a Issue
    task.issue.status = 'cl'
    task.issue.save()

    print(f'Stop issue: {task.issue.number} - {task}')

    stop_timesheet(task)

    remove_aqui_from_tarefas(task)

    write_x_on_tarefas(task)

    # subprocess.run(f'notify-send --hint int:transient:1 "{task}" "{hora_total}"', shell=True)
    return True


class Command(BaseCommand):
    help = 'Stop task.'

    def add_arguments(self, parser):
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')
        parser.add_argument('--task', '-t', type=str, help='Type the number of task.')

    def handle(self, *args, **options):
        stop_task_command(options)
