# My Tasks

Sistema de gerenciamento de tarefas e timesheet.

## Este projeto foi feito com:

* [Django 4.2.3](https://www.djangoproject.com/)
* [Windmill](https://github.com/estevanmaito/windmill-dashboard)

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

### Sobre o git config

```
git config user.name rg3915
git config user.email *************100@*****.com
```

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

### Exportar timesheet

```bash
python manage.py export_timesheet --project='my-tasks'
```