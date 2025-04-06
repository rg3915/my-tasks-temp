import os
import re
from datetime import datetime

from rich import print
from rich.console import Console

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
        ('numb3rs', 'contratualizacao'): 'python ~/gitlab/my-tasks/backend/core/write_changelog.py -c numb3rs -p contratualizacao',
        ('numb3rs', 'plansus'): 'python ~/gitlab/my-tasks/backend/core/write_changelog.py -c numb3rs -p plansus',
        ('colanabola', 'colanabola'): 'python ~/gitlab/my-tasks/backend/core/write_changelog.py -c colanabola -p colanabola',
        ('euroled', None): 'python ~/gitlab/my-tasks/backend/core/write_changelog_euroled.py',
    }

    return changelog_commands.get((customer, project))
