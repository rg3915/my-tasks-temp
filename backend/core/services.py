import json
import os
from datetime import date, datetime, timedelta

import gitlab
from decouple import config
from openpyxl import Workbook, load_workbook, styles
from rich import print

from backend.core.utils import datetime_to_string
from backend.task.models import Issue, Label, Sprint, Task, Timesheet

FOLDER_BASE = '/home/regis/Dropbox/projetos'


def check_if_the_date_already_exists(filename, milestone_title):
    date_format = datetime.now().strftime('%Y-%m-%d')

    # Check if the file exists, and create it if it doesn't
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(f"## {milestone_title}\n")

    # Check if the date already exists in the file
    with open(filename, 'r') as file:
        file_contents = file.read()
        if date_format in file_contents:
            print("Date already exists in the file.")
        else:
            # Append the date to the file
            with open(filename, 'a') as file:
                file.write(f"\n## {date_format}\n\n")
            print(f"Date {date_format} added to the file {filename}.")


def write_on_tarefas(filename, issue, labels, is_bug):
    today = date.today().strftime('%d/%m/%y')

    _labels = ','.join(labels)

    with open(filename, 'a') as f:
        f.write('\n---\n\n')
        f.write(f'[ ] {issue.number} - {issue.title}\n')
        f.write(f'    {_labels}\n')
        f.write(f'    {today}\n\n\n')

        if issue.description:
            f.write(f'    {issue.description}\n\n')

        title = issue.title
        if is_bug:
            title = f'bugfix: {title}'

        f.write(f"    _gadd '{title}. close #{issue.number}'; # gp\n")


def write_changelog_dropbox(issue):
    customer = issue.sprint.project.customer.name
    project = issue.sprint.project.title
    filename = f'{FOLDER_BASE}/{customer}/{project}/changelog/CHANGELOG_{issue.milestone.title}.md'
    print(filename)

    check_if_the_date_already_exists(filename, issue.milestone.title)

    text = f'* {issue.title}. #{issue.number}\n'

    with open(filename, 'r') as f:
        content = f.read()
        # Escreve somente se o texto não existir.
        if text not in content:
            with open(filename, 'a') as f:
                f.write(text)


def save_issue(data):
    labels = Label.objects.filter(label__in=data['labels'])
    sprint = Sprint.objects.filter(project=data['project']).last()

    issue = Issue.objects.create(
        number=data['iid'],
        title=data['title'],
        description=data['description'],
        milestone=data['milestone'],
        sprint=sprint,
        url=data['web_url'],
    )
    for label in labels:
        issue.labels.add(label)

    filename = f'{FOLDER_BASE}/{sprint.project.customer.name}/{sprint.project.title}/tarefas.txt'

    number = data['iid']
    title = data['title']

    print(filename)
    print(number)
    print(title)

    is_bug = False
    if 'bug' in data['labels']:
        is_bug = True

    write_on_tarefas(filename, issue, data['labels'], is_bug)
    return issue


def save_task(issue):
    data = dict(
        title=issue.title,
        project=issue.sprint.project,
        issue=issue,
    )
    Task.objects.create(**data)


def create_timesheet(task, previous_hour):
    now = datetime.now()
    start_time = datetime.now()

    if previous_hour:
        # TODO: verificar se é do mesmo projeto.
        last_hour = Timesheet.objects.first()  # é o último por causa da ordenação.
        start_time = last_hour.end_time
        print('start:', datetime_to_string(start_time - timedelta(hours=3), '%H:%M'))
        print('now:', datetime_to_string(now, '%H:%M'))
    else:
        print(datetime_to_string(start_time, '%H:%M'))

    return Timesheet.objects.create(task=task, start_time=start_time)


def stop_timesheet(task):
    now = datetime.now()

    print(datetime_to_string(now, '%H:%M'))

    # Na verdade não precisa da task.
    timesheet = Timesheet.objects.filter(task=task, end_time__isnull=True).first()
    timesheet.end_time = now
    timesheet.save()


def create_gitlab_issue(args):
    '''
    Requer /etc/rg3915.cfg
    '''
    gl = gitlab.Gitlab.from_config('somewhere', ['/etc/rg3915.cfg'])

    title, body, labels, project, milestone = args.values()

    gl_project = gl.projects.get(project.gitlab_project_id)

    data_dict = {
        "title": f"{title}",
        "description": f"{body}",
        "assignee_id": config('GITLAB_ASSIGNEE_ID'),
        "labels": labels,
        "milestone_id": milestone.original_id,
    }

    response = gl_project.issues.create(data_dict)

    data = json.loads(response.to_json())

    # TESTE
    # data = {
    #     "iid": 7,
    #     "title": "Teste",
    #     "description": "Descrição teste.",
    #     "labels": ["backend", "frontend"],
    #     # "time_stats":
    #     # {
    #     #     "time_estimate": 0,
    #     #     "total_time_spent": 0,
    #     # },
    #     "web_url": "https://gitlab.com/rg3915/my-tasks/-/issues/7",
    # }

    data['project'] = project
    data['milestone'] = milestone

    return data


def export_timesheet_service(project):
    tasks = project.get_tasks()

    customer = project.customer.name
    project = project.title
    timesheet_filename = f'{FOLDER_BASE}/{customer}/{project}/timesheet_teste.xlsx'

    try:
        wb = load_workbook(timesheet_filename)
        ws = wb['timesheet']
    except FileNotFoundError:
        wb = Workbook()
        ws = wb.create_sheet('timesheet')
        wb.save(timesheet_filename)

    new_row = 2

    labels = (
        'data',
        'hora_inicial',
        'hora_final',
        'tempo',
        'tempo_display',
        'issue',
        'title'
    )

    bold_calibri = styles.Font(bold=True, name='Calibri')

    # Set labels and apply font in a loop
    for col, label in enumerate(labels, start=1):
        cell = ws.cell(row=1, column=col, value=label)
        cell.font = bold_calibri

    for task in tasks:
        for timesheet in task.get_timesheets():
            ws.cell(row=new_row, column=1, value=timesheet.date_from_start_time_display)
            ws.cell(row=new_row, column=2, value=timesheet.start_time_display)
            ws.cell(row=new_row, column=3, value=timesheet.end_time_display)
            ws.cell(row=new_row, column=4, value=timesheet.get_hour())
            ws.cell(row=new_row, column=5, value=timesheet.get_hour_display())

            cell = ws.cell(row=new_row, column=6, value=timesheet.task.issue.number)
            cell.alignment = styles.Alignment(horizontal='center')

            ws.cell(row=new_row, column=7, value=timesheet.task.issue.title)

            new_row += 1

    wb.save(timesheet_filename)
