from backend.task.models import Task


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
