"""
m start_task --project='my-tasks' --task=1
"""

import warnings

from django.core.management.base import BaseCommand
from rich import print
from rich.console import Console

from backend.core.services.file_writers import write_tarefas
from backend.core.services.timesheet_service import create_timesheet
from backend.project.models import Project
from backend.task.models import Task, Timesheet

console = Console()

warnings.filterwarnings('ignore')


def start_task_command(options):
    """
    Return a tuple.
    timesheet_not_finalized, timesheet
    """
    # get project
    project = Project.objects.filter(title=options['project']).first()

    # A Task está diretamente relacionada com a Issue.
    # get task
    task = Task.objects.filter(project=project, issue__number=options['task']).first()

    # get timesheet_not_finalized
    timesheet_not_finalized = Timesheet.objects.filter(end_time__isnull=True).first()

    if timesheet_not_finalized:
        print(f'Task: {task.issue.number} - {task}')
        console.print('Error: Existe uma tarefa não finalizada.', style='red')
        return False, False, None
    else:
        print(f'Start issue: {task.issue.number} - {task}')
        # timesheet = create_timesheet(task, options['previous_hour'])
        timesheet = create_timesheet(task)

        write_tarefas(task)

        # if options['previous_hour']:
        #     return True, True, timesheet

        return True, False, timesheet


class Command(BaseCommand):
    help = 'Start task.'

    def add_arguments(self, parser):
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')
        parser.add_argument('--task', '-t', type=str, help='Type the number of task.')
        # parser.add_argument('--previous_hour', '-ph', type=bool, default=False, help='Start new hour with previous hour.')  # noqa E501

    def handle(self, *args, **options):
        start_task_command(options)
