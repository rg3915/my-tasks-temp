"""
python ~/gitlab/my-tasks/backend/core/write_changelog.py -c numb3rs -p contratualizacao
python ~/gitlab/my-tasks/backend/core/write_changelog.py -c numb3rs -p plansus
"""

from datetime import datetime

import click


def check_if_the_date_already_exists(filename):
    date_format = datetime.now().strftime('%Y-%m-%d')

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

            # Nao usa mais
            # subprocess.run(f'tail {filename}', shell=True)


@click.command()
@click.option('--customer', '-c', help='Type customer.')
@click.option('--project', '-p', help='Type project.')
def write_changelog(customer, project):
    BASE_FOLDER = '/home/regis'
    project_folder = ''

    if customer == 'numb3rs':
        project_folder = 'nu'

    filename = f'{BASE_FOLDER}/{project_folder}/{project}/CHANGELOG.md'

    check_if_the_date_already_exists(filename)


if __name__ == '__main__':
    write_changelog()
