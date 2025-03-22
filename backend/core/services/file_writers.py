import subprocess
from datetime import date

from backend.core.services.outros_service import (
    check_if_the_date_already_exists,
    conjugate_infinitive,
    get_changelog_command,
    get_changelog_paths,
)
from backend.task.models import Sprint

FOLDER_BASE = '/home/regis/Dropbox/projetos'


def write_tarefas(task):
    # Escreve lorem na segunda linha depois do match.
    # n;n;n; significa três next.
    sprint = Sprint.objects.filter(project=task.project).last()
    tarefas_filename = f'{FOLDER_BASE}/{sprint.project.customer.name}/{sprint.project.title}/tarefas.txt'

    task = f'{task.issue.number} - {task.title}'

    lorem = 'lorem'
    sed_command = 'sed -i "/\\] ' + task + '/{n;n;n;s/.*/' + lorem + '/}" ' + tarefas_filename
    subprocess.run(sed_command, shell=True)

    # Substitui lorem por AQUI
    asterisco = '\\n    AQUI'
    sed_command = f'sed -i "s/{lorem}/{asterisco}\\n/" {tarefas_filename}'
    subprocess.run(sed_command, shell=True)


def remove_aqui_from_tarefas(task):
    """
    Remove AQUI de tarefas.txt
    """
    sprint = Sprint.objects.filter(project=task.project).last()
    tarefas_filename = f'{FOLDER_BASE}/{sprint.project.customer.name}/{sprint.project.title}/tarefas.txt'

    # sed_command = f'sed -i "s/    AQUI/{{N;d;}}" {tarefas_filename}'
    sed_command = f'sed -i "/    AQUI/{{N;d;}}" {tarefas_filename} && sed -i "s/    AQUI//" {tarefas_filename}'
    subprocess.run(sed_command, shell=True)


def write_x_on_tarefas(task):
    sprint = Sprint.objects.filter(project=task.project).last()
    tarefas_filename = f'{FOLDER_BASE}/{sprint.project.customer.name}/{sprint.project.title}/tarefas.txt'

    task_text = f'{task.issue.number} - {task}'
    # print(task_text)
    escaped_task_text = task_text.replace('/', '\\/')  # Escape any slashes in the task_text
    command = f"sed -i 's/\\[ \\] {escaped_task_text}/\\[x\\] {escaped_task_text}/' {tarefas_filename}"
    subprocess.run(command, shell=True, check=True)


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
