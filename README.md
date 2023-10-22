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

