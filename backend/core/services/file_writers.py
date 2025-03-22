import subprocess


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
