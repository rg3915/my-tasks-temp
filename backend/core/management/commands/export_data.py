from django.core.management.base import BaseCommand

from backend.crm.admin import CustomerResource
from backend.financial.admin import PaymentResource
from backend.project.admin import OwnerResource, ProjectResource
from backend.task.admin import (
    IssueResource,
    MilestoneResource,
    SprintResource,
    TaskResource,
    TimesheetResource
)

PATH = '/home/regis/Dropbox/projetos/mytasks/my-tasks/bkp_dataset'


def export_resource(resource_type, file_name):
    resource = resource_type().export()
    csv_content = resource.csv
    file_path = f'{PATH}/{file_name}.csv'

    with open(file_path, 'w', encoding='utf-8') as csv_file:
        csv_file.write(csv_content)

    print(f"CSV file saved to: {file_path}")


def export_all_resources():
    resources = [
        (CustomerResource, 'customer'),
        (PaymentResource, 'payment'),
        (OwnerResource, 'owner'),
        (ProjectResource, 'project'),
        (MilestoneResource, 'milestone'),
        (SprintResource, 'sprint'),
        (IssueResource, 'issue'),
        (TaskResource, 'task'),
        (TimesheetResource, 'timesheet'),
    ]

    for resource_type, file_name in resources:
        export_resource(resource_type, file_name)


class Command(BaseCommand):
    help = "Export tables via command line."

    def handle(self, *args, **options):
        export_all_resources()
