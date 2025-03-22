import json
import os
import re
from datetime import date, datetime

import gitlab
import requests
from decouple import config
from rich import print
from rich.console import Console

from backend.task.models import Issue, Label, Sprint, Task

console = Console()


FOLDER_BASE = '/home/regis/Dropbox/projetos'


CONJUGATIONS = {
    'adicionar': 'adiciona',
    'aplicar': 'aplica',
    'cadastrar': 'cadastra',
    'calcular': 'calcula',
    'corrigir': 'corrige',
    'criar': 'cria',
    'deletar': 'deleta',
    'editar': 'edita',
    'entregar': 'entrega',
    'enviar': 'envia',
    'gerar': 'gera',
    'imprimir': 'imprime',
    'instalar': 'instala',
    'processar': 'processa',
    'remover': 'remove',
    'retornar': 'retorna',
    'salvar': 'salva',
}


def get_changelog_paths(project) -> list[str]:
    """
    Gera caminho completo dos CHANGELOG.

    Args:
        project (str): Nome do projeto

    Returns:
        list: Lista de caminhos de arquivos de changelog para atualizar
    """

    # Gera o caminho do projeto
    project_path = f'~/{project.project_folder}/CHANGELOG.md'

    # Gera o caminho do Dropbox
    dropbox_path = f'cp ~/{project.project_folder}/CHANGELOG.md ~/Dropbox/projetos/{project.dropbox_folder}/changelog/CHANGELOG.md'

    return [project_path, dropbox_path]


def conjugate_infinitive(sentence):
    # Função para substituir verbos no infinitivo pela forma conjugada
    def replace_verb(match):
        verb = match.group(0)
        conjugated = CONJUGATIONS.get(verb.lower(), verb)  # Busca a forma conjugada em minúsculas

        # Mantém a capitalização se a primeira letra do verbo original for maiúscula
        if verb[0].isupper():
            conjugated = conjugated.capitalize()

        return conjugated

    # Padrão para encontrar verbos no infinitivo
    infinitive_pattern = r'\b(\w+ar|\w+er|\w+ir)\b'

    # Substituir verbos no infinitivo pela conjugação correta
    conjugated_sentence = re.sub(infinitive_pattern, replace_verb, sentence)

    return conjugated_sentence


def check_if_the_date_already_exists(filename, milestone_title):
    date_format = datetime.now().strftime('%Y-%m-%d')

    # Check if the file exists, and create it if it doesn't
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(f'## {milestone_title}\n')

    # Check if the date already exists in the file
    with open(filename, 'r') as file:
        file_contents = file.read()
        if date_format in file_contents:
            print('Date already exists in the file.')
        else:
            # Append the date to the file
            with open(filename, 'a') as file:
                file.write(f'\n## {date_format}\n\n')
            print(f'Date {date_format} added to the file {filename}.')


def get_changelog_command(customer: str, project: str) -> str:
    """
    Gera comando de escrita de changelog baseado no cliente e projeto.

    Args:
        customer (str): Nome do cliente
        project (str): Nome do projeto

    Returns:
        str ou None: Comando para escrever changelog, se aplicável
    """
    changelog_commands = {
        (
            'numb3rs',
            'contratualizacao',
        ): 'python ~/gitlab/my-tasks/backend/core/write_changelog.py -c numb3rs -p contratualizacao',
        ('numb3rs', 'plansus'): 'python ~/gitlab/my-tasks/backend/core/write_changelog.py -c numb3rs -p plansus',
        ('euroled', None): 'python ~/gitlab/my-tasks/backend/core/write_changelog_euroled.py',
    }

    return changelog_commands.get((customer, project))


def write_on_tarefas(filename: str, issue, labels: list[str], is_bug: bool) -> None:
    """
    Escreve detalhes do issue em um arquivo de rastreamento de tarefas
    com tratamento flexível de changelog.
    """
    today = date.today().strftime('%d/%m/%y')
    _labels = ','.join(labels)
    project = issue.sprint.project
    customer = issue.sprint.project.customer.name

    with open(filename, 'a') as f:
        write_issue_header(f, issue, _labels, today, is_bug)
        write_issue_description(f, issue)
        write_changelog_commands(f, customer, project, issue)
        write_task_management_commands(f, project, issue)
        write_git_commands(f, issue)


def write_issue_header(f, issue, labels, today, is_bug):
    # title = f'bugfix: {issue.title}' if is_bug else issue.title
    f.write('\n---\n\n')
    f.write(f'[ ] {issue.number} - {issue.title}\n')
    f.write(f'    {labels}\n')
    f.write(f'    {today}\n\n\n')


def write_issue_description(f, issue):
    if issue.description:
        f.write(f'    {issue.description}\n\n')


def write_changelog_commands(f, customer, project, issue):
    changelog_command = get_changelog_command(customer, project.title)
    if changelog_command:
        f.write(f'    {changelog_command}\n')

    changelog_paths = get_changelog_paths(project)
    conjugated_title = conjugate_infinitive(issue.title)

    f.write(f'    echo "* {conjugated_title}. #{issue.number}" >> {changelog_paths[0]}\n')
    f.write(f'    {changelog_paths[1]}\n')


def write_task_management_commands(f, project, issue):
    f.write(f"\n    cd ~/gitlab/my-tasks; sa; m start_task -p='{project}' -t={issue.number}\n")
    f.write(f'    tail {get_changelog_paths(project)[0]}\n')

    if project == 'ekoospregao':
        f.write(
            f'    workon {issue.sprint.project.customer.name}; python cli/task.py -c start -p {project} -t {issue.number} --previous_hour\n'
        )


def write_git_commands(f, issue):
    conjugated_title = conjugate_infinitive(issue.title)
    f.write(f"\n    _gadd '{conjugated_title}. close #{issue.number}'; # gp\n\n")
    f.write(f"    cd ~/gitlab/my-tasks; sa; m stop_task -p='{issue.sprint.project.title}' -t={issue.number}\n")

    if issue.sprint.project.title == 'ekoospregao':
        f.write(
            f'    workon {issue.sprint.project.customer.name}; python cli/task.py -c end -p {issue.sprint.project.title} -t {issue.number}\n'
        )


# --------------------------


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


def save_task(issue):
    Task.objects.get_or_create(
        title=issue.title,
        project=issue.sprint.project,
        issue=issue,
    )


def save_task_multiple(issues):
    for issue in issues:
        save_task(issue)


def update_task(issue):
    task = Task.objects.filter(issue=issue).first()
    task.title = issue.title
    task.save()


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
