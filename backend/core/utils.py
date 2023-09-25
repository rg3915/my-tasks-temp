import sys
from pprint import pprint

import gitlab
from decouple import config
from faker import Faker

fake = Faker()


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "#" * x, "." * (size - x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    file.write("\n")
    file.flush()


def gen_short_title():
    return fake.sentence(nb_words=3).replace('.', '')


def gen_title():
    return fake.sentence()


def gen_phrase(n=5):
    return ' '.join(fake.texts(nb_texts=n))


def gen_name():
    return fake.first_name()


def gen_company():
    return fake.company()


def make_gitlab_issue(args):
    '''
    Requer /etc/rg3915.cfg
    '''
    gl = gitlab.Gitlab.from_config('somewhere', ['/etc/rg3915.cfg'])

    print('args')
    pprint(args)

    project, command, title, body, labels, milestone, gitlab_project_id, milestone_id = args.values()

    print('project', project)

    gl_project = gl.projects.get(gitlab_project_id)

    data_dict = {
        "title": f"{title}",
        "description": f"{body}",
        "assignee_id": config('GITLAB_ASSIGNEE_ID'),
        "labels": labels,
        "milestone_id": milestone_id,
    }

    pprint(gl_project)

    pprint(data_dict)

    # response = gl_project.issues.create(data_dict)

    # print('response')
    # print(response.iid)
    # print(response.title)
    # print(response.description)

    # data = response.to_json()

    # print('data')
    # pprint(data)

    data = {
        "iid": 7,
        "title": "Teste",
        "description": "Descri\\u00e7\\u00e3o teste.",
        "labels": ["backend", "frontend"],
        "time_stats":
        {
            "time_estimate": 0,
            "total_time_spent": 0,
        },
    }

    # write_on_tarefas(project, tarefas_filename, data, labels, milestone, milestone_v)
