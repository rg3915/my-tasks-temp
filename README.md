# My Tasks

Sistema de gerenciamento de tarefas e timesheet.

## Este projeto foi feito com:

* [Django 4.2.3](https://www.djangoproject.com/)
* [Windmill](https://github.com/estevanmaito/windmill-dashboard)
    * [heroicons](https://heroicons.dev/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://gitlab.com/rg3915/my-tasks.git
cd my-tasks

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python contrib/env_gen.py

python manage.py migrate
python manage.py createsuperuser
```

### DOCS das APIs

[python-gitlab](https://python-gitlab.readthedocs.io/en/stable/)

[Issues API](https://docs.gitlab.com/ee/api/issues.html)

[GitHub REST API](https://docs.github.com/en/rest/issues?apiVersion=2022-11-28#create-an-issue)

### Sobre o git config

```
git config user.name rg3915
git config user.email *************100@*****.com
```

### Gitlab

O Token do Gitlab é configurado em `/etc/rg3915.cfg`

## Comandos

### Criar Issue

```bash
python manage.py create_issue \
--project='my-tasks' \
--title='Criar issue' \
--body='Criar issue por linha de comando.' \
--labels='backend' \
--milestone='1111111'
```

### Editar Issue

```bash
python manage.py update_issue \
--issue=1 \
--project='my-tasks' \
--title='Editado' \
--body='The quick brown fox jumps over the lazy dog.' \
--labels='backend,frontend,bug' \
--milestone='1111111'  # milestone.original_id
```

### Ler Issues

```bash
python manage.py read_issue \
--project='my-tasks' \
--milestone='111111' \
--assignee='rg3915'
```

### Iniciar task

```bash
python manage.py start_task --project='my-tasks' --task=1 -ph=True
```

### Parar task

```bash
python manage.py stop_task --project='my-tasks' --task=1
```

### Exportar timesheet

```bash
python manage.py export_timesheet --project='my-tasks'
```

### Exportar com django-import-export

Vamos fazer isso por linha de comando, via `shell_plus`.

```python
from backend.task.admin import TimesheetResource

dataset = TimesheetResource().export()
```

Ou

```bash
python manage.py export_data
```