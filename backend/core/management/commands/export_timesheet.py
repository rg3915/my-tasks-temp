"""
m export_timesheet --project='my-tasks'
"""

import warnings

from django.core.management.base import BaseCommand

from backend.core.services.timesheet_service import export_timesheet_service
from backend.project.models import Project

warnings.filterwarnings('ignore')


def export_timesheet(options):
    project = Project.objects.filter(title=options['project']).first()
    export_timesheet_service(project)


class Command(BaseCommand):
    help = 'Export Timesheet.'

    def add_arguments(self, parser):
        parser.add_argument('--project', '-p', type=str, help='Type the name of project.')

    def handle(self, *args, **options):
        export_timesheet(options)
