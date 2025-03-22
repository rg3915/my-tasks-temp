import json

import gitlab
import requests
from decouple import config
from rich import print
from rich.console import Console

from backend.core.services.file_writers import write_on_tarefas
from backend.task.models import Issue, Label, Sprint

console = Console()

FOLDER_BASE = '/home/regis/Dropbox/projetos'


def update_issue(data):
    labels = Label.objects.filter(label__in=data['labels'])
    sprint = Sprint.objects.filter(project=data['project']).last()

    issue = Issue.objects.filter(number=data['iid'], sprint__project=data['project']).first()

    payload = dict(
        number=data['iid'],
        title=data['title'],
        description=data['description'],
        milestone=data['milestone'],
    )

    for attr, value in payload.items():
        setattr(issue, attr, value)

    issue.save()

    print(issue)

    issue.labels.clear()
    for label in labels:
        issue.labels.add(label)

    filename = f'{FOLDER_BASE}/{sprint.project.customer.name}/{sprint.project.title}/tarefas.txt'

    is_bug = False
    if 'bug' in data['labels']:
        is_bug = True

    write_on_tarefas(filename, issue, data['labels'], is_bug)
    return issue


def create_gitlab_issue(args):
    """
    Requer /etc/rg3915.cfg
    """
    gl = gitlab.Gitlab.from_config('somewhere', ['/etc/rg3915.cfg'])

    title, body, labels, project, milestone = args.values()

    gl_project = gl.projects.get(project.gitlab_project_id)

    data_dict = {
        'title': f'{title}',
        'description': f'{body}',
        'assignee_id': config('GITLAB_ASSIGNEE_ID'),
        'labels': labels,
        'milestone_id': milestone.original_id,
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


def create_github_issue(args):
    title, body, labels, project, milestone = args.values()

    assignee = 'rg3915'

    repo_owner = project.repository_owner
    repo_name = project.title
    token = project.github_token
    URL = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'

    headers = {'Authorization': f'token {token}'}

    labels = labels.split(',')

    # Create our issue
    issue = {
        'title': title,
        'body': body,
        'assignees': [assignee],
        'labels': labels,
        'milestone': milestone.original_id,
    }

    # Add the issue to our repository
    response = requests.post(URL, headers=headers, json=issue)

    if response.status_code == 201:
        console.print(f'Successfully created Issue "{title}"', style='green')
        data = response.json()

        data['project'] = project
        data['labels'] = labels
        data['iid'] = data['number']
        data['description'] = data['body']
        data['milestone'] = milestone
        data['web_url'] = data['html_url']

        return data

    console.print(f'Could not create Issue "{title}"', style='red')


def update_gitlab_issue(args):
    """
    Requer /etc/rg3915.cfg
    """
    gl = gitlab.Gitlab.from_config('somewhere', ['/etc/rg3915.cfg'])

    id, title, body, labels, project, milestone = args.values()

    gl_project = gl.projects.get(project.gitlab_project_id)

    data_dict = {
        'title': f'{title}',
        'description': f'{body}',
        'assignee_id': config('GITLAB_ASSIGNEE_ID'),
        'labels': labels,
        'milestone_id': milestone.original_id,
    }

    response = gl_project.issues.update(id, data_dict)

    data = response

    data['project'] = project
    data['milestone'] = milestone

    return data


def update_github_issue(args):
    issue, title, body, labels, project, milestone = args.values()

    assignee = 'rg3915'

    repo_owner = project.repository_owner
    repo_name = project.title
    token = project.github_token
    URL = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue}'

    headers = {'Authorization': f'token {token}'}

    labels = labels.split(',')

    issue = {
        'title': title,
        'body': body,
        'assignees': [assignee],
        'labels': labels,
        'milestone': milestone.original_id,
    }

    # Add the issue to our repository
    response = requests.post(URL, headers=headers, json=issue)

    if response.status_code == 200:
        console.print(f'Successfully updated Issue "{title}"', style='green')
        data = response.json()

        data['project'] = project
        data['labels'] = labels
        data['iid'] = data['number']
        data['description'] = data['body']
        data['milestone'] = milestone
        data['web_url'] = data['html_url']

        return data

    console.print(f'Could not update Issue "{title}"', style='red')


def read_gitlab_issue(args):
    """
    Requer /etc/rg3915.cfg
    """
    gl = gitlab.Gitlab.from_config('somewhere', ['/etc/rg3915.cfg'])

    milestone, assignee, project = args.values()

    gl_project = gl.projects.get(project.gitlab_project_id)

    response = gl_project.issues.list(per_page=100, order_by='created_at')
    # response = gl_project.issues.list(per_page=100, milestone='0.0.1', state='opened')
    # response = gl_project.issues.list(per_page=100, order_by='created_at')

    items = []
    for data in response:
        _data = {}
        _data['iid'] = data.iid
        _data['title'] = data.title
        _data['description'] = data.description
        _data['labels'] = data.labels
        _data['web_url'] = data.web_url
        _data['project'] = project
        _data['milestone'] = milestone
        items.append(_data)

    return items


def read_github_issue(args):
    milestone, assignee, project = args.values()

    repo_owner = project.repository_owner
    repo_name = project.title
    token = project.github_token
    URL = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'

    headers = {'Authorization': f'token {token}'}

    # Read issues
    response = requests.get(URL, headers=headers)

    issues = []
    if response.status_code == 200:
        console.print('Successfully read Issues', style='green')

        for data in response.json():
            labels = [item['name'] for item in data['labels']]
            data['project'] = project
            data['labels'] = labels
            data['iid'] = data['number']
            data['description'] = data['body']
            data['milestone'] = milestone
            data['web_url'] = data['html_url']

            issues.append(data)

        return issues

    console.print('Could not read Issues', style='red')


def save_issue(data):
    # Mapeamento de nomes de clientes para seus diretórios
    CUSTOMER_FOLDER_MAPPING = {
        'DVR-Industrial': 'dvr',
        # Outros mapeamentos podem ser adicionados aqui
    }

    # Obter objetos relacionados do banco de dados
    labels = Label.objects.filter(label__in=data['labels'])
    sprint = Sprint.objects.filter(project=data['project']).last()

    # Criar o registro da issue
    issue = Issue.objects.create(
        number=data['iid'],
        title=data['title'],
        description=data['description'],
        milestone=data['milestone'],
        sprint=sprint,
        url=data['web_url'],
    )

    # Adicionar labels à issue
    issue.labels.add(*labels)

    # Determinar o nome da pasta do cliente usando o mapeamento
    customer_name = sprint.project.customer.name
    folder_name = CUSTOMER_FOLDER_MAPPING.get(customer_name, customer_name.lower())

    # Preparar informações para arquivo de tarefas
    filename = f'{FOLDER_BASE}/{folder_name}/{sprint.project.title}/tarefas.txt'
    is_bug = 'bug' in data['labels']

    # Registrar informações para debug (opcional)
    print(f'Gravando issue #{data["iid"]} - {data["title"]} em {filename}')

    # Escrever no arquivo de tarefas
    write_on_tarefas(filename, issue, data['labels'], is_bug)

    return issue


def save_issue_multiple(datas):
    issues = []

    sorted_data = sorted(datas, key=lambda x: x['iid'])

    for data in sorted_data:
        labels = Label.objects.filter(label__in=data['labels'])
        sprint = Sprint.objects.filter(project=data['project']).last()

        issue, _ = Issue.objects.get_or_create(
            number=data['iid'],
            title=data['title'],
            description=data['description'],
            milestone=data['milestone'],
            sprint=sprint,
            url=data['web_url'],
        )

        issues.append(issue)

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
    return issues
